import pyxie
from pyxie import devtool
import pickle
import pyvmath as vmath
import pybullet as p
import os

# import time

# ------------------------------------------------------------
# --pre process

FILENAME = "Lion_Voxel_340.dae"

if os.path.exists("boxinfo.pickle"):
    os.remove("boxinfo.pickle")

if not os.path.exists("boxinfo.pickle"):
    # if True:

    efig = pyxie.editableFigure("efig")
    devtool.loadCollada(FILENAME, efig)

    boxinfo = []
    for i in range(efig.numMeshes):
        aabb = vmath.aabb()
        inverts = efig.getVertexElements(i, pyxie.ATTRIBUTE_ID_POSITION)
        for pos in inverts:
            aabb.insert(pos)
        outverts = []
        for pos in inverts:
            outverts.append(pos - aabb.center)
        efig.setVertexElements(i, pyxie.ATTRIBUTE_ID_POSITION, outverts)
        efig.setJoint(i, position=aabb.center)

        min, max = efig.getMeshAABB(i)
        pos, rot, _ = efig.getJoint(i)
        data = (
            (pos.x, pos.y, pos.z),
            (rot.x, rot.y, rot.z, rot.w),
            (min.x, min.y, min.z),
            (max.x, max.z, max.z),
        )
        boxinfo.append(data)

    with open("boxinfo.pickle", "wb") as f:
        pickle.dump(boxinfo, f)

    efig.mergeMesh()
    efig.saveFigure("Castle_standard")
# ------------------------------------------------------------


pyxie.window(True, 480, 640)

p.connect(p.DIRECT)
p.setGravity(0, 0, -10)

flags = p.URDF_ENABLE_SLEEPING

boxinfo = []
with open("boxinfo.pickle", "rb") as f:
    boxinfo = pickle.load(f)

planeCollisionID = p.createCollisionShape(p.GEOM_PLANE)
plane = p.createMultiBody(
    0,
    baseCollisionShapeIndex=planeCollisionID,
    basePosition=[0, 0, -1],
    flags=p.URDF_ENABLE_SLEEPING,
)

bodies = []

box1 = boxinfo[0]
SCALE = 0.98
shape = p.createCollisionShape(
    p.GEOM_BOX, halfExtents=[box1[3][0] * SCALE, box1[3][1] * SCALE, box1[3][2] * SCALE]
)

for data in boxinfo:
    pos = (data[0][0], data[0][1], data[0][2] + -0.5)
    body = p.createMultiBody(
        baseMass=1, baseCollisionShapeIndex=shape, basePosition=pos
    )
    p.changeDynamics(
        bodyUniqueId=body,
        linkIndex=-1,
        mass=1,
        linearDamping=0.4,
        angularDamping=1,
        restitution=0.8,
    )
    bodies.append(body)


# bodies = []
# for data in boxinfo:
#     body = p.createMultiBody(
#         baseMass=1, baseCollisionShapeIndex=shape, basePosition=data[0]
#     )
#     bodies.append(body)

figure = pyxie.figure("Castle_standard")
cam = pyxie.camera()
cam.position = (0, -2, 1)
cam.target = vmath.vec3(0, 0, 0)

showcase = pyxie.showcase("case")
showcase.add(figure)

FPS = 240
p.setPhysicsEngineParameter(
    fixedTimeStep=1.0 / FPS,
    numSolverIterations=12,
    numSubSteps=3,  # 8 is smooth but not sure abt performance. Lowered substeps actually raise fps
    contactBreakingThreshold=0.00000002,
    useSplitImpulse=0,
    splitImpulsePenetrationThreshold=9999999,
    enableConeFriction=0,
    deterministicOverlappingPairs=0,
    solverResidualThreshold=0.1,
)

stepdt = 1 / FPS
totalstepdt = 0
p.setRealTimeSimulation(0)
ddt = 1.0 / FPS
while True:
    if totalstepdt > stepdt:
        p.stepSimulation()
        while totalstepdt > stepdt:
            totalstepdt -= stepdt

        index = 1
        for bd in bodies:
            pos, rot = p.getBasePositionAndOrientation(bd)
            # Set position here
            # pos = (pos[0] + 1 * pyxie.getElapsedTime(), pos[1], pos[2])
            # p.resetBasePositionAndOrientation(bodyUniqueId=bd, posObj=pos, ornObj=rot)
            figure.setJoint(index, position=pos, rotation=rot)
            index += 1

        # time.sleep(1.0 / FPS)

        # Get collision happened last frame here? Don't know if its cool or not
        # print(len(p.getContactPoints(bodyA=planeCollisionID)))

    dt = pyxie.getElapsedTime()
    totalstepdt += dt

    cam.shoot(showcase)
    pyxie.swap()

    ddt += (dt - ddt) * 0.12
    print(1 / ddt)
