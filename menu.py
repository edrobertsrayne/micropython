class MenuItem:
    def __init__(self, name, callback=None, parent=None):
        self.name = name
        self.callback = callback
        self.parent = parent
        self.children = []
        self.selected = False

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        return child


class MenuSystem:
    def __init__(self, display):
        self.display = display
        self.root = MenuItem("Main Menu")
        self.current_menu = self.root
        self.cursor_pos = 0
        self.scroll_offset = 0
        self.max_lines = 4  # Adjust based on your display height

    def add_menu_item(self, path, callback=None):
        """Add a menu item using a path string like 'Settings/Network/WiFi'"""
        parts = path.split("/")
        current = self.root

        for i, part in enumerate(parts):
            # Check if this item already exists at this level
            found = False
            for child in current.children:
                if child.name == part:
                    current = child
                    found = True
                    break

            if not found:
                # Create new item
                new_item = MenuItem(part, callback if i == len(parts) - 1 else None)
                current.add_child(new_item)
                current = new_item

        return current

    def button_up(self):
        if self.cursor_pos > 0:
            self.cursor_pos -= 1
            if self.cursor_pos < self.scroll_offset:
                self.scroll_offset -= 1
            self.display_menu()

    def button_down(self):
        if self.cursor_pos < len(self.current_menu.children) - 1:
            self.cursor_pos += 1
            if self.cursor_pos >= self.scroll_offset + self.max_lines:
                self.scroll_offset += 1
            self.display_menu()

    def button_forward(self):
        if self.current_menu.children:
            selected_item = self.current_menu.children[self.cursor_pos]
            if selected_item.children:
                # Has submenu, navigate to it
                self.current_menu = selected_item
                self.cursor_pos = 0
                self.scroll_offset = 0
                self.display_menu()
            elif selected_item.callback:
                # Execute callback if it exists
                selected_item.callback()

    def button_back(self):
        if self.current_menu.parent:
            self.current_menu = self.current_menu.parent
            self.cursor_pos = 0
            self.scroll_offset = 0
            self.display_menu()

    def display_menu(self):
        # Clear the display
        self.display.fill(0)

        # Display current menu items
        y = 0
        visible_items = self.current_menu.children[
            self.scroll_offset : self.scroll_offset + self.max_lines
        ]

        for i, item in enumerate(visible_items):
            # Highlight selected item
            if i + self.scroll_offset == self.cursor_pos:
                # Draw selection indicator
                self.display.text(">", 0, y * 10, 1)
                self.display.text(item.name, 10, y * 10, 1)
            else:
                self.display.text(item.name, 10, y * 10, 1)

            # Add submenu indicator if item has children
            if item.children:
                self.display.text(">", 120, y * 10, 1)

            y += 1

        # Update the display
        self.display.show()
