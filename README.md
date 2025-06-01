# Highlight Imprecise Italic Angle

A plugin for the [Glyphs font editor](http://glyphsapp.com/).

Highlights the path segments which angle is not precise (or not closest) to Italic Angle of the selected master and is within observed angle range (±10 degrees around Italic Angle). Also it adds placeholder dots around the nodes to indicate the horizontal direction and position for better node placement where segment's angle will be precise to Italic Angle (or smaller of it if precise angle isn't available).

![](PreviewAnimation.gif)

# Italic Angle

The Italic Angle is taken from Font Info -> Masters. If you work with italic master, the plugin will check the vertical segments and handles around Italic Angle. Also, it is worth noting that even upright styles have Italic Angle parameter set to 0. And if you work with upright master, the plugin will check all the vertical stems and handles that are not precise to 0 degree.

# Highlight

If segment is highlighted, that means that:

- The segment's angle isn't precise to Italic Angle.
- The segment's angle is within the observed range (±10 degrees around Italic Angle).

If segment within the observed range isn't highlighted, that means one of the following cases:

- The segment's angle is precise to Italic Angle.
- The precise Italic Angle for this segments lies between the grid coordinates and it is impossible to place the segment correctly without using fractional coordinates. So, with an integer coordinates, the segment's angle is already closest to Italic Angle, and even one point movement can't make it any closer to Italic Angle.

# Rounding

If the precise angle is not possible to fit because of grid rounding and integer coordinates, there will two coordinates to choose from – with a greater or smaller angle (from Italic Angle). Here is two rules that will be applied in this case:

- For most cases, when ratio is well chosen, the smaller angle will be chosen. It will happen for many popular ratios like 1:5 (11,31°), 1:4 (14,04°), 2:5 (21,8°). So in a case of well chosen ratio there will be only precise or not precise angle, without "almost" precise angle case where the rounding will be needed.
- If precise angle is less than 0.1 point from coordinate with a greater angle, and greater angle is not greater of precise italic angle + 0.1°, then this coordinate with greater angle will be chosen. It will happen for less popular ratios like 3:14 (12°), 3:10 (16,7°), 3:20 (8,53°). So in case of the angles with such a ratios there will be a lot of situations where angle is almost precise and it make more sense to round it up when the difference from precise angle is like just 0.02 degree.

# Distance

The distance from a node to the placeholder dot is displayed in number next to the placeholder dot, so it is easier to know how much the node should be moved to fit the correct position. For example, if you see the number 4, you need to press the left or right arrow key 4 times. It makes the correction faster.

# Background

The issue of path correction after interpolation is always relevant, especially for italic styles. Usually the glyph shape has its own differences in different masters, so after interpolation (and more often after extrapolation) there are possible kinks, broken rounded nodes, and deviations from the Italic Angle. Read more about the issue in topic [Is there a quick way to fix paths after interpolation?](https://forum.glyphsapp.com/t/is-there-a-quick-way-to-fix-paths-after-interpolation/3311). Usually, RMX Tools is used to correct such errors. On the other hand, *Highlight Imprecise Italic Angle* is more designed for manual review of each glyph, because sometimes it should be estimated by eye and the correction is not always needed.
