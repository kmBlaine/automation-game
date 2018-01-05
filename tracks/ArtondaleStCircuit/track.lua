--Example Automation Track

--You Can use 0, 1, -1 instead.
local STRAIGHT = 0
local LEFT = 1
local RIGHT = -1


Track =
{
    Name = "Artondale Street Circuit",
    --Track Image Info
    --Track Image must be 1280 x 720
    --Start Position on the Image x,y from Top Left
    Start = { 895, 684 },

    --How many pixels per meter ( Pixels / Length )
    --Measure a long straight and then manipulate from there
    Scale = 138.5712813 / 661.85,


    Layout = {STRAIGHT, LEFT, STRAIGHT, RIGHT, STRAIGHT, RIGHT, STRAIGHT, LEFT, STRAIGHT, LEFT, STRAIGHT, LEFT, STRAIGHT, LEFT, STRAIGHT, RIGHT, STRAIGHT, LEFT, RIGHT, STRAIGHT},-- Straight 0 , Corner Left 1, Corner Right -1
    LayoutInfo = {87.9, 105.945, 14.4, 84.319, 26.4, 94.2658, 31, 94.4717, 333.5, 63.115, 166, 31.866, 54, 29.005, 363.5, 50.4117, 6.4, 55.4535, 37.0503, 151.2},-- Straight Length [m] or Corner Angle [°]
    CornerRadius = {0, 6.9, 0, 12, 0, 16.2, 0, 19.7, 0, 257.8, 0, 257.5, 0, 246.4, 0, 17, 0, 13.3, 101.8, 0},-- Corner Radius [m], 0 for Straight
    Slope = {-2.28, 0, 6.94, 5.66, 0, -7.5, -6.45, -3.17, -4.5, 4.23, 2.41, 0.7, 0, -1.6, -7.43, -12, -15.62, -15.5, -9.11, -1.98},-- [%] (-: descending, +: climbing)
    Sportiness = {0, 0, 0, 0, 0, 2, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 3, 3, 1, 2},-- 0: no problems, 5: problems with untame car
    Camber = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},-- [°] (positive values: banking to left /, negative: banking to right \)
    Split1 = 300,
    Split2 = 500,
}
