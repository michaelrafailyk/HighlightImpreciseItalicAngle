# Highlight Imprecise Italic Angle

A plugin for the [Glyphs font editor](http://glyphsapp.com/).

Highlights the path segments which angle is not precise (or not closest) to Italic Angle of the selected master and is within observed angle range (±10 degrees around Italic Angle). Also it adds placeholder dots around the nodes to indicate the horizontal direction and position for better node placement where segment's angle will be closest to Italic Angle.

![](PreviewAnimation.gif)

# Colors

- Red color means that the segment most likely needs correction.
- Yellow color means that the segment angle before and after correction will remain the same. For example: precise angle is 12, angle before correction is 11.7, angle after correction will be 12.3, so the difference is still the same.

# Italic Angle

The Italic Angle is taken from Font Info -> Masters. If you work with italic master, the plugin will check the vertical segments and handles around Italic Angle. Also, it is worth noting that even upright styles have Italic Angle parameter set to 0. And if you work with upright master, the plugin will check all the vertical stems and handles that are not precise to 0 degree.

# Precise angle after rounding to grid coordinates

If segment isn't highlighted, that means one of two following situations:

- The segment's angle is precise to Italic Angle.
- The Italic Angle for this segments lies between the grid coordinates and it is impossible to place the segment without using fractional coordinates. So, with an integer coordinates, the segment's angle is already closest to Italic Angle, and even one point movement can't make it any closer to Italic Angle.

# Distance

The distance from a node to the placeholder dot is displayed in number next to the placeholder dot, so it is easier to know how much the node should be moved to fit the correct position. For example, if you see the number 4, you need to press the left or right arrow key 4 times. It makes the correction faster.

# Background

The issue of path correction after interpolation is always relevant, especially for italic styles. Usually the glyph shape has its own differences in different masters, so after interpolation (and more often after extrapolation) there are possible kinks, broken rounded nodes, and deviations from the Italic Angle. Read more about the issue in topic [Is there a quick way to fix paths after interpolation?](https://forum.glyphsapp.com/t/is-there-a-quick-way-to-fix-paths-after-interpolation/3311). Usually, RMX Tools is used to correct such errors. On the other hand, *Highlight Imprecise Italic Angle* is more designed for manual review of each glyph, because sometimes it should be estimated by eye and the correction is not always needed.
