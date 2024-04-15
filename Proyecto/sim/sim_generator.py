import Sofa
from pressure_gen import PressureGen    


plugins=['Sofa.Component.AnimationLoop','Sofa.Component.IO.Mesh','Sofa.Component.Visual',
    'Sofa.Component.Constraint.Lagrangian.Solver','Sofa.Component.Mass','Sofa.Component.ODESolver.Backward',
    'Sofa.Component.StateContainer','Sofa.Component.Topology.Container.Dynamic','Sofa.GL.Component.Rendering3D',
    'Sofa.GL.Component.Shader','Sofa.Component.LinearSolver.Iterative','Sofa.Component.Mapping.Linear',
    'Sofa.Component.MechanicalLoad','Sofa.Component.SolidMechanics.Spring','Sofa.Component.SolidMechanics.FEM.Elastic',
    'Sofa.Component.Engine.Select','Sofa.Component.Engine.Transform','Sofa.Component.Constraint.Projective',
    'Sofa.Component.LinearSolver.Direct','Sofa.Component.SolidMechanics.FEM.HyperElastic'
    ]

def createScene(root):
    root.gravity=[0,0,0]
    root.dt=0.01    
    root.addObject("RequiredPlugin", pluginName=plugins)    
    root.addObject('DefaultAnimationLoop')
    root.addObject('VisualStyle', displayFlags="showVisual showBehaviorModels showForceFields")
    root.addObject('MeshGmshLoader',name='volume',filename='./assets/cuerpo.msh')

    actuador = root.addChild('actuador')
    actuador.addObject('EulerImplicitSolver',rayleighStiffness='0.1',rayleighMass='0.1')
    # actuador.addObject('StaticSolver')
    actuador.addObject('CGLinearSolver', name="CG Solver", iterations="100", tolerance="1e-05", threshold="1e-05")    
    actuador.addObject('MechanicalObject', name="StateVectors", template="Vec3",src="@../volume")
    actuador.addObject('TetrahedronSetTopologyContainer', name="volume_tetra", src="@../volume")
    actuador.addObject('TetrahedronSetGeometryAlgorithms',template="Vec3",name="GeomAlgo")
    actuador.addObject('TetrahedronSetTopologyModifier',name="Modifier")
    actuador.addObject('UniformMass',totalMass="45.0e-3")
    #actuador.addObject('TetrahedronFEMForceField',template='Vec3',name='FEM',method='large',poissonRatio='0.47',youngModulus='21000')
    actuador.addObject('TetrahedronHyperelasticityFEMForceField', template='Vec3',name="HyperElasticMaterial", materialName="MooneyRivlin", ParameterSet="382000 96000 446000")
    actuador.addObject('MeshSTLLoader',name='fixedMesh',filename='./assets/fijador.stl')
    actuador.addObject('MeshROI',name='fixedROI',src='@fixedMesh',drawMesh='1',drawTetrahedra='1',doUpdate='0',position='@StateVectors.position',tetrahedra='@../volume.tetrahedra',ROIposition='@fixedMesh.position',ROItriangles='@fixedMesh.triangles')
    actuador.addObject('MeshSTLLoader',name='tipMesh',filename='./assets/ROI.stl')
    actuador.addObject('MeshROI',name='tipROI',src='@tipMesh',drawMesh='1',drawTetrahedra='1',doUpdate='0',position='@StateVectors.position',tetrahedra='@../volume.tetrahedra',ROIposition='@tipMesh.position',ROItriangles='@tipMesh.triangles')
    actuador.addObject('FixedConstraint',name='fixed',indices='@fixedROI.indices')

    cavity = actuador.addChild('cavity')
    cavity.addObject('MeshSTLLoader',name='cavity',filename='./assets/Inserto 1 Reducido.stl')
    cavity.addObject('TriangleSetTopologyContainer',name='surface_tris',src='@cavity')
    cavity.addObject('TriangleSetGeometryAlgorithms',name='GeomAlgo',template='Vec3')
    cavity.addObject('MechanicalObject',name='StateVectors',template='Vec3',src='@cavity')
    cavity.addObject('SurfacePressureForceField',name='cavityPressure',pressure='0',pulseMode='false',drawForceScale='0.0001',useTangentStiffness='false')
    cavity.addObject('BarycentricMapping')
    
    actuador.addObject(PressureGen(node=actuador))

    return root