""" This module helps you to print easily a tree. """

from typing import List, Union
from prettypi.utils import Color, Style


class TreeNode:
    """TreeNode class to create a tree.

    **Features:**

    - Use the add_child method to add a child to the node.
    - Add color and style to the node with the set_color and set_style methods.
    - Use the display method to display the tree.

    :param value: The value of the node
    :type value: str
    :param color: The color of the node, defaults to None
    :type color: Color, optional
    :param style: The style of the node, defaults to None
    :type style: Style, optional

    **Example:**

    .. code-block:: python

        from prettypi.pretty_tree import TreeNode
        from prettypi.utils import Color, Style

        root = TreeNode("Root", color=Color.RED, style=Style.BOLD)
        child1 = TreeNode("Child1", color=Color.GREEN, style=Style.UNDERLINE)
        child2 = TreeNode("Child2", color=Color.GREEN, style=Style.UNDERLINE)

        child1.add_child(TreeNode("Child1.1"))
        child1.add_child(TreeNode("Child1.2"))

        root.add_child(child1)
        root.add_child(child2)

        root.display()

    """

    def __init__(self, value: str = "", color: Color = None, style: Style = None):
        self.value = value
        self.children = []
        self.color = color
        self.style = style

    def add_child(self, child: Union["TreeNode", List["TreeNode"]]):
        """Add a child or a list of children to the node.

        :param child: The child or the list of children to add
        :type child: Union["TreeNode", list["TreeNode"]]

        :raises TypeError: child must be of type TreeNode or list[TreeNode]

        **Example:**

        .. code-block:: python

            root = TreeNode("Root")

            child1 = TreeNode("Child1", color=Color.GREEN, style=Style.UNDERLINE)
            child1.add_child(TreeNode("Child1.1"))

            root.add_child(child1)

        """
        if not isinstance(child, List):
            child = [child]
        for one_child in child:
            if not isinstance(one_child, TreeNode):
                raise TypeError("child must be of type TreeNode or list[TreeNode]")
            self.children.append(one_child)

    def set_color(self, color: Color):
        """Set the color of the node.

        :param color: The color of the node
        :type color: Color

        :raises ValueError: Invalid color

        **Example:**

        .. code-block:: python

            root = TreeNode("Root")
            root.set_color(Color.RED)

        """
        if not isinstance(color, Color):
            raise ValueError("Invalid color")
        self.color = color

    def set_style(self, style: Style):
        """Set the style of the node.

        :param style: The style of the node
        :type style: Style

        :raises ValueError: Invalid style

        **Example:**

        .. code-block:: python

            root = TreeNode("Root")
            root.set_style(Style.BOLD)

        """
        if not isinstance(style, Style):
            raise ValueError("Invalid style")
        self.style = style

    def _compute_value(self):
        """Compute the value of the node with the color and style.

        :return: The value of the node with the color and style
        :rtype: str

        """
        color = self.color if self.color else ""
        style = self.style if self.style else ""
        if self.color or self.style:
            return f"{color}{style}{self.value}{Color.RESET}"
        return self.value

    def _display_tree(self, prefix="first", is_last=False):
        """Display the tree. (recursive function)

        :param prefix: The prefix of the node, defaults to "first"
        :type prefix: str, optional
        :param is_last: If the node is the last child, defaults to False
        :type is_last: bool, optional


        """
        elbow = "└──"
        pipe = "│  "
        tee = "├──"
        blank = "   "
        first = ""

        value = self._compute_value()

        if prefix == "first":
            print(value)
            prefix = first
        else:
            print(prefix + (elbow if is_last else tee) + value)
            prefix += blank if is_last else pipe

        for i, child in enumerate(self.children):
            is_last = i == len(self.children) - 1
            TreeNode._display_tree(child, prefix, is_last)

    def display(self):
        """Display the tree.

        **Example:**

        .. code-block:: python

            root = TreeNode("Root")
            root.display()

        """
        self._display_tree()
