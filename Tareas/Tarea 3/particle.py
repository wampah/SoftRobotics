import Sofa

plugins=['Sofa.Component.LinearSolver.Iterative','Sofa.Component.Mass',
    'Sofa.Component.ODESolver.Forward','Sofa.Component.SolidMechanics.Spring',
    'Sofa.Component.StateContainer', 'Sofa.Component.Topology.Container.Constant',
    'Sofa.Component.Visual', 'Sofa.Component.Constraint.Projective',
    'Sofa.Component.MechanicalLoad'
    ]

def createScene(root):
    root.gravity=[0, -9.81, 0]
    root.dt=0.001    
    root.addObject("RequiredPlugin", pluginName=plugins)

    root.addObject('DefaultAnimationLoop')
    root.addObject('VisualStyle', displayFlags="showBehavior showVisual")
    root.addObject('EulerExplicitSolver')
    root.addObject('CGLinearSolver', name="CG Solver", iterations="50", tolerance="1e-06", threshold="1e-06")
    
    particles = root.addChild('particles')
    particles.addObject('MechanicalObject', name="Particles", template="Vec3",position="0 0 0  0 -0.1 0", showIndices="1", showObject="1")
    particles.addObject('MeshTopology', edges='0 1')    
    particles.addObject('FixedConstraint', name="FixedConstraint", indices="0")
    particles.addObject('UniformMass', totalMass=1.0)
    particles.addObject('MeshSpringForceField', stiffness=1,damping=0.1)
    return root