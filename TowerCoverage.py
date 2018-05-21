from Tower import *
import random
import matplotlib.patches as patches

#Question 1
def coverageFromN(n, width, height):
    """
    Determine total coverage achieved from n Towers in a grid with width and height. Place n towers, trimming their
    coverage so that they do not overlap.
    Parameters:
        n (int) - number of towers
        width (int) - width of total area to cover
        height (int) - height of total area to cover

    Returns:
        towers (list) - Towers that do not overlap
        untrimmed (list) - Towers before they were trimmed
        area (int) - Area covered by n towers
    """
    assert isinstance(n, int) and n > 0, "n must be positive int"
    assert isinstance(width, int) and width > 0, "Overall area width must be positive int"
    assert isinstance(height, int) and height > 0, "Overall area height must be positive int"

    total_area = width * height
    towers = []
    untrimmed = []
    #add first tower to the empty space
    new_tower = makeTower(width, height)
    towers.append(new_tower)
    untrimmed.append(new_tower)
    while len(towers) < n:
        #if area is fully covered, no more towers needed
        if (getArea(towers) == total_area):
            break

        new_tower = makeTower(width, height)
        improved_tower = getMaxTower(new_tower, towers)
        if(improved_tower == None):
            continue

        towers.append(improved_tower)
        untrimmed.append(new_tower)

    return towers, untrimmed, getArea(towers)

#Question 2
def getArea(towers):
    """
    Get the area of the towers already placed
    Parameters:
        towers (list) - list of towers placed

    Returns:
        int of sum of area of all towers
    """
    assert isinstance(towers, list), "towers isn't list"
    area = 0
    for t in towers:
        assert isinstance(t, Tower), "towers contains a non-Tower object"
        area += t.area
    return area


#Question 3
def fullCoverage(width, height):
    """
    Determines the number of towers needed to achieve full coverage of the grid with dimensions width and height.
    Follows same steps as covereageFromN to place towers, trim them, and repeat. The difference is that this function will
    exit when the coverage area is completely filled, instead of after n towers have been placed.
    Parameters:
        width (int) - width of total area to cover
        height (int) - height of total area to cover

    Returns:
        towers (list) - Towers that do not overlap
        untrimmed (list) - Towers before they were trimmed
        count (int) - number of towers needed to achieve full coverage
    """
    assert isinstance(width, int) and width > 0, "Overall area width must be positive int"
    assert isinstance(height, int) and height > 0, "Overall area height must be positive int"

    total_area = width * height
    towers = []
    untrimmed = []
    count = 0
    new_tower = makeTower(width, height)
    # towers is empty, so first one can't overlap
    towers.append(new_tower)
    count += 1
    while getArea(towers) != total_area:
        new_tower = makeTower(width, height)
        improved_tower = getMaxTower(new_tower, towers)
        if (improved_tower == None):
            continue

        towers.append(improved_tower)
        untrimmed.append(new_tower)
        count += 1

    return towers, untrimmed, count


def makeTower(width, height):
    """
    Make a tower with width and height uniformly distributed between 1 and width and 1 and height respectively
    starting at a valid point within the grid.
    Parameters:
        width (int) - maximum possible width
        height (int) - maximum possible height

    Returns:
        Tower (Tower) - The tower that was created
    """
    assert isinstance(width, int) and width > 0, "Overall grid width must be a positve int"
    assert isinstance(height, int) and height > 0, "Overall grid height must be a positive int"

    # w and h are the towers width and height within the grid
    # w and h are strictly less than width and height respectively
    w = random.randint(1, width)
    h = random.randint(1, height)

    # starting point tuple start must keep w and h within the grid
    startx = random.randint(0, width - w)
    starty = random.randint(0, height - h)
    start = (startx, starty)

    return Tower(start, w, h)


def getMaxTower(new_tower, towers):
    """
    Place the new_tower into the grid by finding the maximum non-overlapping area with all the towers in towers
    and returning a Tower with that area. Creates a list of all possible towers that can be placed, then chooses the
    one with maximum area.
    Parameters:
        new_tower (Tower) - Tower to be placed
        towers (list) - List of towers already placed

    Returns:
        Tower to be placed that doesn't overlap with any others, or None if this isn't possible
    """
    assert isinstance(new_tower, Tower), "new_tower needs to be a Tower"
    assert isinstance(towers, list), "towers must be list of Towers"
    possible_towers = [new_tower]
    for t in towers:
        assert isinstance(t, Tower), "item in towers is not Tower"
        new_possibilities = []
        # check every possible tower created by trimming against every other tower
        for possible in possible_towers:
            # if the current possible tower overlaps, trim it and check it against rest
            if(possible.overlaps(t)):
                cur_possibilities = trim(possible, t)
                #cur_possibilities is empty if new_tower is fully inside t
                if(len(cur_possibilities) == 0):
                    continue
                new_possibilities += cur_possibilities
            # otherwise check it against rest
            else:
                new_possibilities.append(possible)
        possible_towers = new_possibilities

    # Return the trimmed tower with maximum area
    if (len(possible_towers) > 0):
        return getTowerWithMaxArea(possible_towers)

    # Else if there are no towers that don't overlap, return None
    return None


def trim(new_tower, old_tower):
    """
    Trims new_tower so that it doesn't overlap old_tower anymore. It does this by checking each side to see if it overlaps.
    If it does, it cuts new_tower so that it doesn't overlap old_tower and adding this to a list of Towers. This list is
    returned at the end.
    Parameters:
        new_tower (Tower) - Tower to be trimmed
        old_tower (Tower) - Tower already in the grid

    Returns:
        Biggest Tower that doesn't overlap with old_tower, or None if not possible
    """
    # Check all 4 sides to see which overlap and add possible to a list
    # if the side overlaps, create a new Tower that doesn't overlap
    trimmed = []
    # left side overlaps but isn't completely overlapped
    if(new_tower.left < old_tower.right and new_tower.right > old_tower.right):
        temp_start = (old_tower.right, new_tower.bot)
        temp_width = new_tower.width - (old_tower.right - new_tower.left)
        temp_height = new_tower.height
        temp = Tower(temp_start, temp_width, temp_height)
        trimmed.append(temp)

    # right side overlaps but isn't completely overlapped
    if(new_tower.right > old_tower.left and new_tower.left < old_tower.left):
        temp_start = new_tower.start
        temp_width = old_tower.left - new_tower.left
        temp_height = new_tower.height
        temp = Tower(temp_start, temp_width, temp_height)
        trimmed.append(temp)

    # bottom side overlaps but isn't completely overlapped
    if(new_tower.bot < old_tower.top and new_tower.top > old_tower.top):
        temp_start = (new_tower.left, old_tower.top)
        temp_width = new_tower.width
        temp_height = new_tower.height - (old_tower.top - new_tower.bot)
        temp = Tower(temp_start, temp_width, temp_height)
        trimmed.append(temp)

    # top side overlaps but isn't completely overlapped
    if (new_tower.top > old_tower.bot and new_tower.bot < old_tower.bot):
        temp_start = new_tower.start
        temp_width = new_tower.width
        temp_height = old_tower.bot - new_tower.bot
        temp = Tower(temp_start, temp_width, temp_height)
        trimmed.append(temp)

    # Return the largest trimmed tower
    return trimmed


def getTowerWithMaxArea(towers):
    """
    Get the Tower with maximum area among the list of towers
    Parameters:
        towers (list) - list of towers

    Returns:
        Tower that has max area
    """
    assert isinstance(towers, list) and len(towers) > 0, "towers must be list with at least one item"
    max_area = 0
    for t in towers:
        assert isinstance(t, Tower), "tower must contain only Towers"
        if (t.area > max_area):
            max_area = t.area
            max_tower = t
    return max_tower


def towersToRects(towers):
    """
    Given a list of towers, represent them as rectangles using the matplotlib library.
    Parameters:
        towers (list) - List of towers to be drawn
    Returns:
        list of patches that can then be plotted by matplotlib
    """
    assert isinstance(towers, list), "towers must be a list of Towers"
    rectangles = []
    for i, tower in enumerate(towers):
        assert isinstance(tower, Tower), "towers must only contain Towers"
        # Tower object already has the necessary inputs to make a Rectangle patch
        rect = patches.Rectangle(tower.start, tower.width, tower.height, facecolor=getColor(i),
                                 alpha=.8, edgecolor="black")
        rectangles.append(rect)

    return rectangles

def getColor(i):
    """
    Gives a color for an index
    Parameters:
        i (int) - index of a tower

    Returns:
        color (string) - color of that tower
    """
    colors = ["red", "orange", "yellow", "chartreuse", "green", "teal", "cyan", "blue", "navy",
              "purple", "violet", "black", "darkred"]
    return colors[i % len(colors)]