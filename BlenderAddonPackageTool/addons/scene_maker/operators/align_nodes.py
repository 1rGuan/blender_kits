import bpy
from copy import copy

def check(cls, context):
    space = context.space_data
    if space.type != 'NODE_EDITOR':
        cls.poll_message_set("Current editor is not a node editor.")
        return False
    if space.node_tree is None:
        cls.poll_message_set("No node tree was found in the current node editor.")
        return False
    if space.node_tree.library is not None:
        cls.poll_message_set("Current node tree is linked from another .blend file.")
        return False
    return True

def check_not_empty(cls, context):
    if not context.space_data.edit_tree.nodes:
        cls.poll_message_set("Current node tree does not contain any nodes.")
        return False
    return True

def get_nodes_links(context):
    tree = context.space_data.edit_tree
    return tree.nodes, tree.links

class OT_AlignNodes(bpy.types.Operator):
    '''Align the selected nodes neatly in a row/column'''
    bl_idname = "scene_maker.align_nodes"
    bl_label = "Align Nodes"
    bl_options = {'REGISTER', 'UNDO'}
    

    @classmethod
    def poll(cls, context):
        return check(cls, context) and check_not_empty(cls, context)

    def execute(self, context):
        nodes, links = get_nodes_links(context)
        margin = bpy.context.scene.scene_maker.margin

        selection = []
        for node in nodes:
            if node.select and node.type != 'FRAME':
                selection.append(node)

        # If no nodes are selected, align all nodes
        active_loc = None
        if not selection:
            selection = nodes
        elif nodes.active in selection:
            active_loc = copy(nodes.active.location)  # make a copy, not a reference

        # Check if nodes should be laid out horizontally or vertically
        # use dimension to get center of node, not corner
        x_locs = [n.location.x + (n.dimensions.x / 2) for n in selection]
        y_locs = [n.location.y - (n.dimensions.y / 2) for n in selection]
        x_range = max(x_locs) - min(x_locs)
        y_range = max(y_locs) - min(y_locs)
        mid_x = (max(x_locs) + min(x_locs)) / 2
        mid_y = (max(y_locs) + min(y_locs)) / 2
        horizontal = x_range > y_range

        # Sort selection by location of node mid-point
        if horizontal:
            selection = sorted(selection, key=lambda n: n.location.x + (n.dimensions.x / 2))
        else:
            selection = sorted(selection, key=lambda n: n.location.y - (n.dimensions.y / 2), reverse=True)

        # Alignment
        current_pos = 0
        for node in selection:
            current_margin = margin
            current_margin = current_margin * 0.5 if node.hide else current_margin  # use a smaller margin for hidden nodes

            if horizontal:
                node.location.x = current_pos
                current_pos += current_margin + node.dimensions.x
                node.location.y = mid_y + (node.dimensions.y / 2)
            else:
                node.location.y = current_pos
                current_pos -= (current_margin * 0.3) + node.dimensions.y  # use half-margin for vertical alignment
                node.location.x = mid_x - (node.dimensions.x / 2)

        # If active node is selected, center nodes around it
        if active_loc is not None:
            active_loc_diff = active_loc - nodes.active.location
            for node in selection:
                node.location += active_loc_diff
        else:  # Position nodes centered around where they used to be
            locs = ([n.location.x + (n.dimensions.x / 2) for n in selection]
                    ) if horizontal else ([n.location.y - (n.dimensions.y / 2) for n in selection])
            new_mid = (max(locs) + min(locs)) / 2
            for node in selection:
                if horizontal:
                    node.location.x += (mid_x - new_mid)
                else:
                    node.location.y += (mid_y - new_mid)

        return {'FINISHED'}
