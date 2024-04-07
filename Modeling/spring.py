#!/usr/bin/env python

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData
)
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersModeling import vtkRotationalExtrusionFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)

def create_cell_array(number_of_points):
    cell_array = vtkCellArray()
    cell_array.InsertNextCell(number_of_points)
    for i in range(number_of_points):
        cell_array.InsertCellPoint(i)
    
    return cell_array

def create_points(point_data):
    points = vtkPoints()
    for point in point_data:
        points.InsertPoint(point["id"], point["coords"])

    return points

def main():
    colors = vtkNamedColors()

    # Create the RenderWindow, Renderer and Interactor.
    #
    renderer = vtkRenderer()
    renWin = vtkRenderWindow()
    renWin.AddRenderer(renderer)

    iren = vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Create the spring profile (a circle).
    #
    point_data = [
        {"id": 0, "coords": (1.0, 0.0, 0.0)},
        {"id": 1, "coords": (1.0732, 0.0, -0.1768)},
        {"id": 2, "coords": (1.25, 0.0, -0.25)},
        {"id": 3, "coords": (1.4268, 0.0, -0.1768)},
        {"id": 4, "coords": (1.5, 0.0, 0.00)},
        {"id": 5, "coords": (1.4268, 0.0, 0.1768)},
        {"id": 6, "coords": (1.25, 0.0, 0.25)},
        {"id": 7, "coords": (1.0732, 0.0, 0.1768)},
    ]

    points = create_points(point_data)

    poly = create_cell_array(number_of_points=8)

    profile = vtkPolyData()
    profile.SetPoints(points)
    profile.SetPolys(poly)

    # Extrude the profile to make a spring.
    #
    extrude = vtkRotationalExtrusionFilter()
    extrude.SetInputData(profile)
    extrude.SetResolution(360)
    extrude.SetTranslation(6)
    extrude.SetDeltaRadius(1.0)
    extrude.SetAngle(6*360.0)  # six revolutions

    normals = vtkPolyDataNormals()
    normals.SetInputConnection(extrude.GetOutputPort())
    normals.SetFeatureAngle(60)

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(normals.GetOutputPort())

    spring = vtkActor()
    spring.SetMapper(mapper)
    spring.GetProperty().SetColor(colors.GetColor3d("PowderBlue"))
    spring.GetProperty().SetDiffuse(0.7)
    spring.GetProperty().SetSpecular(0.4)
    spring.GetProperty().SetSpecularPower(20)
    spring.GetProperty().BackfaceCullingOn()

    # Add the actors to the renderer, set the background and size.
    #
    renderer.AddActor(spring)
    renderer.SetBackground(colors.GetColor3d("Burlywood"))
    renWin.SetSize(640, 512)
    renWin.SetWindowName('Spring')

    renderer.ResetCamera()
    renderer.GetActiveCamera().Azimuth(90)

    # Render the image.
    #
    renWin.Render()
    iren.Start()


if __name__ == '__main__':
    main()