from PySide6 import QtCore

from cmlibs.zinc.field import Field, FieldFindMeshLocation
from cmlibs.zinc.glyph import Glyph
from cmlibs.zinc.graphics import Graphics
from cmlibs.zinc.node import Node
from cmlibs.zinc.result import RESULT_OK
from cmlibs.zinc.scenecoordinatesystem import SCENECOORDINATESYSTEM_LOCAL

from cmlibs.maths.vectorops import sub, add, div, angle, cross, axis_angle_to_rotation_matrix, normalize, matrix_mult, reshape, magnitude
from cmlibs.utils.zinc.finiteelement import create_nodes
from cmlibs.utils.zinc.general import ChangeManager
from cmlibs.utils.zinc.region import determine_appropriate_glyph_size
from cmlibs.utils.zinc.scene import scene_get_or_create_selection_group

from cmlibs.widgets.definitions import ManipulationMode
from cmlibs.widgets.errors import HandlerError
from cmlibs.widgets.handlers.keyactivatedhandler import KeyActivatedHandler


class ConstrainedNodeEditor(KeyActivatedHandler):

    def __init__(self, key_code):
        super(ConstrainedNodeEditor, self).__init__(key_code)
        self._model = None
        self._alignKeyPressed = False
        self._align_mode = ManipulationMode.NONE

        self._edit_node = None
        self._edit_graphics = None
        self._edit_element_dimension = None

        self._last_mouse_pos = None
        self._pixel_scale = -1.0

        self._find_mesh_location_field = None
        self._node_graphics = []

    def enter(self):
        self._align_mode = ManipulationMode.NONE
        self._pixel_scale = self._scene_viewer.get_pixel_scale()

    def leave(self):
        scene = self._scene_viewer.get_zinc_sceneviewer().getScene()
        with ChangeManager(scene):
            selectionGroup = self._scene_viewer.get_or_create_selection_group()
            selectionGroup.clear()

            while len(self._node_graphics):
                graphic = self._node_graphics.pop(0)
                graphic_scene = graphic.getScene()
                graphic_scene.removeGraphics(graphic)
                del graphic

    def set_model(self, model):
        if hasattr(model, 'new') and hasattr(model, 'update'):
            self._model = model
        else:
            raise HandlerError('Given model does not have the required API for node editing')

    def _select_node(self, node):
        nodeset = node.getNodeset()
        fm = nodeset.getFieldmodule()
        with ChangeManager(fm):
            selection_group = self._scene_viewer.get_or_create_selection_group()
            selection_group.clear()
            nodeset_group = selection_group.getOrCreateNodesetGroup(nodeset)
            nodeset_group.addNode(node)

    def _fix_node_to_mesh(self, fc, node, coordinates, element_dimension):
        found_element, xi = self._find_mesh_location_field.evaluateMeshLocation(fc, element_dimension)
        if found_element.isValid():
            fc.setMeshLocation(found_element, xi)
            result, values = coordinates.evaluateReal(fc, 3)
            fc.setNode(node)
            coordinates.assignReal(fc, values)
            return values

        return [0, 0, 0]

    def mouse_press_event(self, event):
        button = event.button()
        if button == QtCore.Qt.MouseButton.LeftButton:
            event_x = event.x() * self._pixel_scale
            event_y = event.y() * self._pixel_scale

            datapoint = self._scene_viewer.get_nearest_node(event_x, event_y)
            element = self._scene_viewer.get_nearest_element(event_x, event_y)
            datapoint_graphics = self._scene_viewer.get_nearest_graphics_datapoint(event_x, event_y)
            if datapoint.isValid() and element.isValid() and datapoint_graphics is not None:
                self._last_mouse_pos = [event_x, event_y]
                self._edit_node = datapoint
                self._edit_graphics = datapoint_graphics
                self._edit_element_dimension = element.getDimension()
                self._find_mesh_location_field.setSearchMesh(element.getMesh())
                if len(self._node_graphics) == 0:
                    coordinates = datapoint_graphics.getCoordinateField()
                    fm = coordinates.getFieldmodule()
                    region = fm.getRegion()
                    scene = datapoint_graphics.getScene()
                    glyph_width = determine_appropriate_glyph_size(region, coordinates)
                    default_orientation = [[10, 0, 0], [0, 10, 0], [0, 0, 10]]
                    with ChangeManager(fm):
                        orientation_field = fm.createFieldConstant(reshape(default_orientation, 9))

                    if self._model:
                        orientation_field = self._model.parameter(datapoint, name='orientation')

                    self._node_graphics = _create_orientation_axes(scene, coordinates, glyph_width, orientation_field, domain=Field.DOMAIN_TYPE_DATAPOINTS)

                    if self._model:
                        label_field = self._model.parameter(datapoint, name='label')
                        self._node_graphics.append(_create_label_graphic(scene, coordinates, glyph_width, label_field, domain=Field.DOMAIN_TYPE_DATAPOINTS))

                self._select_node(datapoint)

                return
            elif datapoint.isValid() and datapoint_graphics is not None:
                self._edit_node = datapoint
                self._edit_graphics = datapoint_graphics
                self._edit_element_dimension = None
                self._last_mouse_pos = [event_x, event_y]
                return

            edit_graphics = self._scene_viewer.get_nearest_graphics_element(event_x, event_y)
            if element.isValid() and edit_graphics is not None and datapoint_graphics is None:
                self._last_mouse_pos = [event_x, event_y]

                mesh = element.getMesh()
                coordinates = edit_graphics.getCoordinateField()
                fm = coordinates.getFieldmodule()
                scene = edit_graphics.getScene()

                far_location = self._scene_viewer.unproject(event_x, -event_y, -1.0)
                near_location = self._scene_viewer.unproject(event_x, -event_y, 1.0)
                initial_location = div(add(near_location, far_location), 2.0)

                fc = fm.createFieldcache()
                with ChangeManager(fm):
                    created_nodes = create_nodes(coordinates, [initial_location], 'datapoints')

                    if len(created_nodes) == 1:
                        placing_node = created_nodes[0]
                    else:
                        print('bad things.')

                    if self._find_mesh_location_field is None:
                        self._find_mesh_location_field = fm.createFieldFindMeshLocation(coordinates, coordinates, mesh)
                        self._find_mesh_location_field.setSearchMode(FieldFindMeshLocation.SEARCH_MODE_NEAREST)

                    fc.setNode(placing_node)
                    selection_group = scene_get_or_create_selection_group(scene)
                    mesh_group = selection_group.getOrCreateMeshGroup(mesh)
                    mesh_group.addElement(element)
                    self._find_mesh_location_field.setSearchMesh(mesh_group)
                    self._fix_node_to_mesh(fc, placing_node, coordinates, element.getDimension())
                    if self._model:
                        self._model.new(placing_node, coordinates)

                    selection_group.clear()
                    del mesh_group
                    del selection_group
        else:
            self._last_mouse_pos = None

    def mouse_move_event(self, event):
        if self._edit_node:
            mousePos = self.get_scaled_event_position(event)
            update_last_mouse_pos = True
            nodeset = self._edit_node.getNodeset()
            fieldmodule = nodeset.getFieldmodule()
            with ChangeManager(fieldmodule):
                editCoordinateField = coordinateField = self._edit_graphics.getCoordinateField()
                localScene = self._edit_graphics.getScene()  # need set local scene to get correct transformation
                if coordinateField.getCoordinateSystemType() != Field.COORDINATE_SYSTEM_TYPE_RECTANGULAR_CARTESIAN:
                    editCoordinateField = fieldmodule.createFieldCoordinateTransformation(coordinateField)
                    editCoordinateField.setCoordinateSystemType(Field.COORDINATE_SYSTEM_TYPE_RECTANGULAR_CARTESIAN)
                fieldcache = fieldmodule.createFieldcache()
                fieldcache.setNode(self._edit_node)
                componentsCount = coordinateField.getNumberOfComponents()
                result, initialCoordinates = editCoordinateField.evaluateReal(fieldcache, componentsCount)
                if result == RESULT_OK:
                    for c in range(componentsCount, 3):
                        initialCoordinates.append(0.0)
                    pointattr = self._edit_graphics.getGraphicspointattributes()
                    editVectorField = vectorField = pointattr.getOrientationScaleField()
                    pointBaseSize = pointattr.getBaseSize(3)[1][0]
                    pointScaleFactor = pointattr.getScaleFactors(3)[1][0]
                    if editVectorField.isValid() and (vectorField.getNumberOfComponents() == 3 * componentsCount) \
                            and (pointBaseSize == 0.0) and (pointScaleFactor != 0.0):
                        if vectorField.getCoordinateSystemType() != Field.COORDINATE_SYSTEM_TYPE_RECTANGULAR_CARTESIAN:
                            editVectorField = fieldmodule.createFieldCoordinateTransformation(vectorField, coordinateField)
                            editVectorField.setCoordinateSystemType(Field.COORDINATE_SYSTEM_TYPE_RECTANGULAR_CARTESIAN)
                        result, initialVector = editVectorField.evaluateReal(fieldcache, 3 * componentsCount)
                        # initialTipCoordinates = [(initialCoordinates[c] + initialVector[c] * pointScaleFactor) for c in range(3)]
                        initial_position = self._scene_viewer.unproject(self._last_mouse_pos[0], -self._last_mouse_pos[1], -1.0, SCENECOORDINATESYSTEM_LOCAL, localScene)
                        final_position = self._scene_viewer.unproject(mousePos[0], -mousePos[1], -1.0, SCENECOORDINATESYSTEM_LOCAL, localScene)
                        # finalVector = [(finalTipCoordinates[c] - initialCoordinates[c]) / pointScaleFactor for c in range(3)]
                        diff = magnitude(sub(self._last_mouse_pos, mousePos))
                        if diff == 0.0:
                            update_last_mouse_pos = False
                        else:
                            theta = 10*angle(final_position, initial_position)
                            # print(f'angle: {theta}')
                            axis = normalize(cross(initial_position, final_position))
                            # print(f'axis: {axis}')
                            mx = axis_angle_to_rotation_matrix(axis, theta)
                            final_vector = matrix_mult(mx, reshape(initialVector, (3, 3)))
                            result = editVectorField.assignReal(fieldcache, reshape(final_vector, 9))
                            self._model.update(self._edit_node, parameter='orientation')
                    elif self._edit_element_dimension is not None:
                        windowCoordinates = self._scene_viewer.project(initialCoordinates[0], initialCoordinates[1], initialCoordinates[2], SCENECOORDINATESYSTEM_LOCAL, localScene)
                        xa = self._scene_viewer.unproject(self._last_mouse_pos[0], -self._last_mouse_pos[1], windowCoordinates[2], SCENECOORDINATESYSTEM_LOCAL, localScene)
                        xb = self._scene_viewer.unproject(mousePos[0], -mousePos[1], windowCoordinates[2], SCENECOORDINATESYSTEM_LOCAL, localScene)
                        finalCoordinates = [(initialCoordinates[c] + xb[c] - xa[c]) for c in range(3)]
                        result = editCoordinateField.assignReal(fieldcache, finalCoordinates)
                        position = self._fix_node_to_mesh(fieldcache, self._edit_node, editCoordinateField, self._edit_element_dimension)
                        if self._model:
                            self._model.update(self._edit_node, parameter='coordinate')
                    del editVectorField
                del editCoordinateField
                del fieldcache

            if update_last_mouse_pos:
                self._last_mouse_pos = mousePos

    def mouse_release_event(self, event):
        self._last_mouse_pos = None
        if self._edit_node:
            if event.button() == QtCore.Qt.MouseButton.LeftButton:
                self._edit_node = None
                self._edit_graphics = None


def _define_node_axis_fields(node, region, coordinates):
    fm = region.getFieldmodule()
    fc = fm.createFieldcache()
    with ChangeManager(fm):
        coordinates = coordinates.castFiniteElement()
        node_derivatives = [Node.VALUE_LABEL_D_DS1, Node.VALUE_LABEL_D_DS2, Node.VALUE_LABEL_D_DS3]
        node_axis_initial_values = [[10, 0, 0], [0, 10, 0], [0, 0, 10]]
        node_axis_fields = [[fm.createFieldNodeValue(coordinates, nodeDerivative, 1)] for nodeDerivative in node_derivatives]

        fc.setNode(node)

        component_count = coordinates.getNumberOfComponents()
        result, value = coordinates.evaluateReal(fc, component_count)

        label_field = fm.createFieldStoredString('')

        nodes = node.getNodeset()
        node_template = nodes.createNodetemplate()
        node_template.defineField(coordinates)
        node_template.defineField(label_field)
        for value_label in node_derivatives:
            node_template.setValueNumberOfVersions(coordinates, -1, value_label, 1)

        node.merge(node_template)
        coordinates.assignReal(fc, value)
        for index, value_label in enumerate(node_derivatives):
            node_axis_fields[index][0].setName(f"node_value_{value_label}")
            coordinates.setNodeParameters(fc, -1, value_label, 1, node_axis_initial_values[index])

    return node_axis_fields


def _create_orientation_axes(scene, coordinates, glyph_width, orientation_field, domain=Field.DOMAIN_TYPE_NODES, display_node_orientation=1):
    node_orientation_graphics = []
    with ChangeManager(scene):
        orientation_glyph = scene.createGraphicsPoints()
        node_orientation_graphics.append(orientation_glyph)
        orientation_glyph.setFieldDomainType(domain)
        orientation_glyph.setCoordinateField(coordinates)
        point_attr = orientation_glyph.getGraphicspointattributes()
        point_attr.setGlyphShapeType(Glyph.SHAPE_TYPE_AXES_SOLID_COLOUR)
        point_attr.setBaseSize([0.0, glyph_width, glyph_width])
        # point_attr.setScaleFactors([derivativeScales[i], 0.0, 0.0])
        point_attr.setOrientationScaleField(orientation_field)

        orientation_glyph.setName('displayNodeOrientation')

        orientation_glyph.setSelectMode(Graphics.SELECT_MODE_DRAW_SELECTED if (display_node_orientation == 1) else Graphics.SELECT_MODE_ON)
        # orientation_glyph.setVisibilityFlag(bool(display_node_derivatives) and node_derivative_label in display_node_derivative_labels)

    return node_orientation_graphics


def _create_label_graphic(scene, coordinates, glyph_width, label_field, domain=Field.DOMAIN_TYPE_NODES, display_node_label=1):
    with ChangeManager(scene):
        glyph = scene.createGraphicsPoints()
        glyph.setFieldDomainType(domain)
        glyph.setCoordinateField(coordinates)
        point_attr = glyph.getGraphicspointattributes()
        # point_attr.setScaleFactors([derivativeScales[i], 0.0, 0.0])
        point_attr.setLabelField(label_field)
        point_attr.setGlyphOffset([glyph_width, 0.0, 0.0])
        # font = point_attr.getFont()
        # point_size = font.getPointSize()
        # font.setPointSize(int(point_size * glyph_width + 0.5))

        glyph.setName('displayNodeLabel')

        glyph.setSelectMode(Graphics.SELECT_MODE_DRAW_SELECTED if (display_node_label == 1) else Graphics.SELECT_MODE_ON)
        # glyph.setVisibilityFlag(bool(display_node_derivatives) and node_derivative_label in display_node_derivative_labels)

    return glyph
