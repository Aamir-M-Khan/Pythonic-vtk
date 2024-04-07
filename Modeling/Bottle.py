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
from vtkmodules.vtkFiltersCore import (
    vtkStripper,
    vtkTubeFilter
)
from vtkmodules.vtkFiltersModeling import vtkRotationalExtrusionFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


def set_color(color):
    colors = vtkNamedColors()
    return colors.GetColor3d(color)

def create_vtk_renderer(actor, color):
    renderer = vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(set_color(color))

    renderer.GetActiveCamera().SetPosition(1, 0, 0)
    renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
    renderer.GetActiveCamera().SetViewUp(0, 0, 1)
    renderer.ResetCamera()
    renderer.GetActiveCamera().Azimuth(30)
    renderer.GetActiveCamera().Elevation(30)
    return renderer

def create_actor(mapper, color):
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(set_color(color))
    actor.GetProperty().SetDiffuse(0.7)
    actor.GetProperty().SetSpecular(0.4)
    actor.GetProperty().SetSpecularPower(20)
    actor.GetProperty().BackfaceCullingOn()
    return actor

def create_tube_filter(input_connection, number_of_sides, radius):
    tubes = vtkTubeFilter()
    tubes.SetInputConnection(input_connection)
    tubes.SetNumberOfSides(number_of_sides)
    tubes.SetRadius(radius)
    return tubes

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

    # Create the bottle profile.
    #

    point_data = [
        {"id": 0, "coords": (0.01, 0.0, 0.0)},
        {"id": 1, "coords": (1.5, 0.0, 0.0)},
        {"id": 2, "coords": (1.5, 0.0, 3.5)},
        {"id": 3, "coords": (1.25, 0.0, 3.75)},
        {"id": 4, "coords": (0.75, 0.0, 4.00)},
        {"id": 5, "coords": (0.6, 0.0, 4.35)},
        {"id": 6, "coords": (0.7, 0.0, 4.65)},
        {"id": 7, "coords": (1.0, 0.0, 4.75)},
        {"id": 8, "coords": (1.0, 0.0, 5.0)},
        {"id": 9, "coords": (0.2, 0.0, 5.0)}
    ]
    
    points = create_points(point_data)

    lines = create_cell_array(number_of_points=10)

    profile = vtkPolyData()
    profile.SetPoints(points)
    profile.SetLines(lines)

    # Extrude the profile to make the bottle.
    #
    extrude = vtkRotationalExtrusionFilter()
    extrude.SetInputData(profile)
    extrude.SetResolution(120)

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(extrude.GetOutputPort())

    bottle = create_actor(mapper, 'Mint')

    # Sisplay the profile.
    stripper = vtkStripper()
    stripper.SetInputData(profile)

    tubes = create_tube_filter(input_connection=stripper.GetOutputPort(), number_of_sides=11, radius=0.05)

    profileMapper = vtkPolyDataMapper()
    profileMapper.SetInputConnection(tubes.GetOutputPort())

    profileActor = create_actor(profileMapper, 'Tomato')

    # Add the actors to the renderer, set the background and size.
    #
    renderer.AddActor(bottle)
    renderer.AddActor(profileActor)
    renderer.SetBackground(colors.GetColor3d('Burlywood'))

    renWin.SetSize(640, 480)
    renWin.SetWindowName('Bottle')
    renWin.Render()

    renderer.GetActiveCamera().SetPosition(1, 0, 0)
    renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
    renderer.GetActiveCamera().SetViewUp(0, 0, 1)
    renderer.ResetCamera()
    renderer.GetActiveCamera().Azimuth(30)
    renderer.GetActiveCamera().Elevation(30)

    # Render the image.
    #
    renWin.Render()
    iren.Start()


if __name__ == '__main__':
    main()