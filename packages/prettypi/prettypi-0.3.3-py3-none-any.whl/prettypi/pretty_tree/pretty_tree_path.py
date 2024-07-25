""" This module contains the TreePath class to create a tree of a path. """

from dataclasses import dataclass
import os
from prettypi.pretty_tree.pretty_tree import TreeNode
from prettypi.utils import Color, Style


@dataclass
class Config:
    """Configuration class for the TreePath class

    :param folder_color: The color of the folder, defaults to None
    :type folder_color: Color, optional
    :param folder_style: The style of the folder, defaults to Style.BOLD
    :type folder_style: Style, optional
    :param file_color: The color of the file, defaults to None
    :type file_color: Color, optional
    :param file_style: The style of the file, defaults to None
    :type file_style: Style, optional

    :raises ValueError: If arguments are not of the expected type

    """

    folder_color: Color = None
    folder_style: Style = Style.BOLD
    file_color: Color = None
    file_style: Style = None

    def __post_init__(self):
        if self.folder_color is not None and not isinstance(self.folder_color, Color):
            raise ValueError(
                f"Expected folder_color to be of type Color, got {type(self.folder_color)}"
            )
        if self.folder_style is not None and not isinstance(self.folder_style, Style):
            raise ValueError(
                f"Expected folder_style to be of type Style, got {type(self.folder_style)}"
            )
        if self.file_color is not None and not isinstance(self.file_color, Color):
            raise ValueError(
                f"Expected file_color to be of type Color, got {type(self.file_color)}"
            )
        if self.file_style is not None and not isinstance(self.file_style, Style):
            raise ValueError(
                f"Expected file_style to be of type Style, got {type(self.file_style)}"
            )


class TreePath(TreeNode):
    """TreePath class to create a tree of a path

    **Features:**

    - Use TreePath to create a tree of a path.
    - Use the display method to display the tree.
    - Add color and style to the folder and file with the config parameter.

    :param path: The path to create the tree
    :type path: str
    :param config: The configuration of the tree, defaults to Config()
    :type config: Config, optional

    **Example:**

    .. code-block:: python

            from prettypi.pretty_tree import TreePath
            from prettypi.utils import Color, Style

            config = Config(folder_color=Color.RED, folder_style=Style.BOLD)
            tree = TreePath("path/to/folder", config=config)
            tree.display()

    """

    def __init__(self, path: str, config: Config = Config()):
        self.abs_path = os.path.abspath(path)

        if not isinstance(config, Config):
            raise ValueError(
                f"Expected config to be of type Config, got {type(config)}"
            )

        self.config = config
        self.color = self.config.folder_color
        self.style = self.config.folder_style

        TreeNode.__init__(
            self,
            os.path.basename(path),
            color=self.config.folder_color,
            style=self.config.folder_style,
        )
        self._create_tree()

    def _create_tree(self):
        """Recursive function to create the tree"""
        for item in os.listdir(self.abs_path):
            if os.path.isdir(os.path.join(self.abs_path, item)):
                child = TreePath(os.path.join(self.abs_path, item))
                self.add_child(child)
            else:
                self.add_child(TreeNode(item))

    def _apply_config(self):
        """Apply the config to the tree"""
        self.color = self.config.folder_color
        self.style = self.config.folder_style
        for child in self.children:
            if isinstance(child, TreePath):
                child.set_config(self.config)
                TreePath._apply_config(child)
            else:
                child.color = self.config.file_color
                child.style = self.config.file_style

    def set_config(self, config: Config):
        """Set the configuration of the tree

        :param config: The configuration of the tree
        :type config: Config

        **Example:**

        .. code-block:: python

            from prettypi.pretty_tree import TreePath, Config
            from prettypi.utils import Color, Style

            config = Config(folder_color=Color.RED, folder_style=Style.BOLD)
            tree = TreePath("path/to/folder")
            tree.set_config(config)

        """
        if not isinstance(config, Config):
            raise ValueError(
                f"Expected config to be of type Config, got {type(config)}"
            )
        self.config = config

    def display(self):
        """Display the tree

        **Example:**

        .. code-block:: python

                tree = TreePath("path/to/folder")
                tree.display()

        """
        self._apply_config()
        TreeNode.display(self)
