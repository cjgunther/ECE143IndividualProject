class Tower:
    """
    Tower Class
    Represents a communication tower that has a rectangular coverage area.
    """

    def __init__(self, start, width, height):
        """
        Initializes the tower
        Parameters:
            start (tuple) - Tower starts at bottom left corner (x,y)
            width (int) - width of the tower (x)
            height (int) - height of the tower (y)
        """
        assert isinstance(start, tuple), "start must be a tuple"
        assert len(start) == 2, "start must have 2 arguments"
        assert start[0] >= 0 and start[1] >= 0, "start coordinates must be positive"
        assert isinstance(width, int) and width > 0, "width must be positive"
        assert isinstance(height, int) and height > 0, "height must be positive"
        self.start = start
        self.width = width
        self.height = height


    def __repr__(self):
        """
        Represents the tower as a string
        """
        return "Tower(%s, %d, %d)" % (self.start, self.width, self.height)


    @property
    def left(self):
        """
        Left of the tower
        """
        return self.start[0]


    @property
    def right(self):
        """
        Right of the tower
        """
        return self.start[0] + self.width


    @property
    def bot(self):
        """
        Bottom of the tower
        """
        return self.start[1]


    @property
    def top(self):
        """
        Top of the tower
        """
        return self.start[1] + self.height


    @property
    def area(self):
        """
        Gets the area of the tower
        """
        return self.width * self.height


    def overlaps(self, other):
        """
        Checks if two towers overlap
        Parameters:
            other (Tower) - Tower that is being checked against self for overlap

        Returns:
            True if self overlaps other, else False
        """
        assert isinstance(other, Tower), "other is not a Tower"
        #if self lies outside the range of other, return False
        if((self.bot >= other.top) or (self.top <= other.bot) or
                   (self.left >= other.right) or (self.right <= other.left)):
            return False
        #else return True
        return True
