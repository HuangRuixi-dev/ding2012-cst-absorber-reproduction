'# MWS Version: Version 2023.4 - Apr 26 2023 - ACIS 32.0.1 -

'# length = mm
'# frequency = GHz
'# time = ns
'# frequency range: fmin = 5 fmax = 40
'# created = '[VERSION]2023.4|32.0.1|20230426[/VERSION]


'@ 01_units_parameters

'[VERSION]2023.4|32.0.1|20230426[/VERSION]
StoreParameter "P", "7.2"
StoreParameter "Wb", "6.9"
StoreParameter "Wt", "0.65"
StoreParameter "H", "20"
StoreParameter "N", "80"
StoreParameter "tm", "0.05"
StoreParameter "td", "0.2"
StoreParameter "epsr", "22"
StoreParameter "tand", "0.18"
With Units
.Geometry "mm"
.Frequency "GHz"
.Time "ns"
End With
Solver.FrequencyRange "5", "40"
ChangeSolverType "HF Frequency Domain"

'@ 02_materials

'[VERSION]2023.4|32.0.1|20230426[/VERSION]
With Material
.Reset 
.Name "Dielectric"
.Type "Normal"
.Epsilon "epsr"
.Mue "1"
.TanD "tand"
.TanDFreq "10"
.TanDGiven "True"
.TanDModel "ConstTanD"
.Colour "0.45", "0.3", "0.7"
.Create 
End With
With Material
.Reset 
.Name "Copper"
.Type "Lossy metal"
.Epsilon "1"
.Mue "1"
.Kappa "5e7"
.Colour "0.9", "0.65", "0.2"
.Create 
End With

'@ 03_geometry

'[VERSION]2023.4|32.0.1|20230426[/VERSION]
With Brick
.Reset 
.Name "ground"
.Component "pyramid"
.Material "Copper"
.Xrange "-(P)/2", "(P)/2"
.Yrange "-(P)/2", "(P)/2"
.Zrange "-0.05", "0"
.Create 
End With
With Brick
.Reset 
.Name "d_000"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(0/(N-1)))/2", "(Wb*(Wt/Wb)^(0/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(0/(N-1)))/2", "(Wb*(Wt/Wb)^(0/(N-1)))/2"
.Zrange "0*(td+tm)", "0*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_000"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(0/(N-1)))/2", "(Wb*(Wt/Wb)^(0/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(0/(N-1)))/2", "(Wb*(Wt/Wb)^(0/(N-1)))/2"
.Zrange "0*(td+tm)+td", "0*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_001"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(1/(N-1)))/2", "(Wb*(Wt/Wb)^(1/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(1/(N-1)))/2", "(Wb*(Wt/Wb)^(1/(N-1)))/2"
.Zrange "1*(td+tm)", "1*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_001"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(1/(N-1)))/2", "(Wb*(Wt/Wb)^(1/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(1/(N-1)))/2", "(Wb*(Wt/Wb)^(1/(N-1)))/2"
.Zrange "1*(td+tm)+td", "1*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_002"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(2/(N-1)))/2", "(Wb*(Wt/Wb)^(2/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(2/(N-1)))/2", "(Wb*(Wt/Wb)^(2/(N-1)))/2"
.Zrange "2*(td+tm)", "2*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_002"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(2/(N-1)))/2", "(Wb*(Wt/Wb)^(2/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(2/(N-1)))/2", "(Wb*(Wt/Wb)^(2/(N-1)))/2"
.Zrange "2*(td+tm)+td", "2*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_003"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(3/(N-1)))/2", "(Wb*(Wt/Wb)^(3/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(3/(N-1)))/2", "(Wb*(Wt/Wb)^(3/(N-1)))/2"
.Zrange "3*(td+tm)", "3*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_003"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(3/(N-1)))/2", "(Wb*(Wt/Wb)^(3/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(3/(N-1)))/2", "(Wb*(Wt/Wb)^(3/(N-1)))/2"
.Zrange "3*(td+tm)+td", "3*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_004"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(4/(N-1)))/2", "(Wb*(Wt/Wb)^(4/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(4/(N-1)))/2", "(Wb*(Wt/Wb)^(4/(N-1)))/2"
.Zrange "4*(td+tm)", "4*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_004"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(4/(N-1)))/2", "(Wb*(Wt/Wb)^(4/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(4/(N-1)))/2", "(Wb*(Wt/Wb)^(4/(N-1)))/2"
.Zrange "4*(td+tm)+td", "4*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_005"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(5/(N-1)))/2", "(Wb*(Wt/Wb)^(5/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(5/(N-1)))/2", "(Wb*(Wt/Wb)^(5/(N-1)))/2"
.Zrange "5*(td+tm)", "5*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_005"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(5/(N-1)))/2", "(Wb*(Wt/Wb)^(5/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(5/(N-1)))/2", "(Wb*(Wt/Wb)^(5/(N-1)))/2"
.Zrange "5*(td+tm)+td", "5*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_006"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(6/(N-1)))/2", "(Wb*(Wt/Wb)^(6/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(6/(N-1)))/2", "(Wb*(Wt/Wb)^(6/(N-1)))/2"
.Zrange "6*(td+tm)", "6*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_006"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(6/(N-1)))/2", "(Wb*(Wt/Wb)^(6/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(6/(N-1)))/2", "(Wb*(Wt/Wb)^(6/(N-1)))/2"
.Zrange "6*(td+tm)+td", "6*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_007"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(7/(N-1)))/2", "(Wb*(Wt/Wb)^(7/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(7/(N-1)))/2", "(Wb*(Wt/Wb)^(7/(N-1)))/2"
.Zrange "7*(td+tm)", "7*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_007"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(7/(N-1)))/2", "(Wb*(Wt/Wb)^(7/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(7/(N-1)))/2", "(Wb*(Wt/Wb)^(7/(N-1)))/2"
.Zrange "7*(td+tm)+td", "7*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_008"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(8/(N-1)))/2", "(Wb*(Wt/Wb)^(8/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(8/(N-1)))/2", "(Wb*(Wt/Wb)^(8/(N-1)))/2"
.Zrange "8*(td+tm)", "8*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_008"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(8/(N-1)))/2", "(Wb*(Wt/Wb)^(8/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(8/(N-1)))/2", "(Wb*(Wt/Wb)^(8/(N-1)))/2"
.Zrange "8*(td+tm)+td", "8*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_009"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(9/(N-1)))/2", "(Wb*(Wt/Wb)^(9/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(9/(N-1)))/2", "(Wb*(Wt/Wb)^(9/(N-1)))/2"
.Zrange "9*(td+tm)", "9*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_009"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(9/(N-1)))/2", "(Wb*(Wt/Wb)^(9/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(9/(N-1)))/2", "(Wb*(Wt/Wb)^(9/(N-1)))/2"
.Zrange "9*(td+tm)+td", "9*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_010"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(10/(N-1)))/2", "(Wb*(Wt/Wb)^(10/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(10/(N-1)))/2", "(Wb*(Wt/Wb)^(10/(N-1)))/2"
.Zrange "10*(td+tm)", "10*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_010"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(10/(N-1)))/2", "(Wb*(Wt/Wb)^(10/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(10/(N-1)))/2", "(Wb*(Wt/Wb)^(10/(N-1)))/2"
.Zrange "10*(td+tm)+td", "10*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_011"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(11/(N-1)))/2", "(Wb*(Wt/Wb)^(11/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(11/(N-1)))/2", "(Wb*(Wt/Wb)^(11/(N-1)))/2"
.Zrange "11*(td+tm)", "11*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_011"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(11/(N-1)))/2", "(Wb*(Wt/Wb)^(11/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(11/(N-1)))/2", "(Wb*(Wt/Wb)^(11/(N-1)))/2"
.Zrange "11*(td+tm)+td", "11*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_012"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(12/(N-1)))/2", "(Wb*(Wt/Wb)^(12/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(12/(N-1)))/2", "(Wb*(Wt/Wb)^(12/(N-1)))/2"
.Zrange "12*(td+tm)", "12*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_012"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(12/(N-1)))/2", "(Wb*(Wt/Wb)^(12/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(12/(N-1)))/2", "(Wb*(Wt/Wb)^(12/(N-1)))/2"
.Zrange "12*(td+tm)+td", "12*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_013"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(13/(N-1)))/2", "(Wb*(Wt/Wb)^(13/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(13/(N-1)))/2", "(Wb*(Wt/Wb)^(13/(N-1)))/2"
.Zrange "13*(td+tm)", "13*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_013"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(13/(N-1)))/2", "(Wb*(Wt/Wb)^(13/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(13/(N-1)))/2", "(Wb*(Wt/Wb)^(13/(N-1)))/2"
.Zrange "13*(td+tm)+td", "13*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_014"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(14/(N-1)))/2", "(Wb*(Wt/Wb)^(14/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(14/(N-1)))/2", "(Wb*(Wt/Wb)^(14/(N-1)))/2"
.Zrange "14*(td+tm)", "14*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_014"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(14/(N-1)))/2", "(Wb*(Wt/Wb)^(14/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(14/(N-1)))/2", "(Wb*(Wt/Wb)^(14/(N-1)))/2"
.Zrange "14*(td+tm)+td", "14*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_015"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(15/(N-1)))/2", "(Wb*(Wt/Wb)^(15/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(15/(N-1)))/2", "(Wb*(Wt/Wb)^(15/(N-1)))/2"
.Zrange "15*(td+tm)", "15*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_015"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(15/(N-1)))/2", "(Wb*(Wt/Wb)^(15/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(15/(N-1)))/2", "(Wb*(Wt/Wb)^(15/(N-1)))/2"
.Zrange "15*(td+tm)+td", "15*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_016"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(16/(N-1)))/2", "(Wb*(Wt/Wb)^(16/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(16/(N-1)))/2", "(Wb*(Wt/Wb)^(16/(N-1)))/2"
.Zrange "16*(td+tm)", "16*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_016"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(16/(N-1)))/2", "(Wb*(Wt/Wb)^(16/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(16/(N-1)))/2", "(Wb*(Wt/Wb)^(16/(N-1)))/2"
.Zrange "16*(td+tm)+td", "16*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_017"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(17/(N-1)))/2", "(Wb*(Wt/Wb)^(17/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(17/(N-1)))/2", "(Wb*(Wt/Wb)^(17/(N-1)))/2"
.Zrange "17*(td+tm)", "17*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_017"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(17/(N-1)))/2", "(Wb*(Wt/Wb)^(17/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(17/(N-1)))/2", "(Wb*(Wt/Wb)^(17/(N-1)))/2"
.Zrange "17*(td+tm)+td", "17*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_018"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(18/(N-1)))/2", "(Wb*(Wt/Wb)^(18/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(18/(N-1)))/2", "(Wb*(Wt/Wb)^(18/(N-1)))/2"
.Zrange "18*(td+tm)", "18*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_018"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(18/(N-1)))/2", "(Wb*(Wt/Wb)^(18/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(18/(N-1)))/2", "(Wb*(Wt/Wb)^(18/(N-1)))/2"
.Zrange "18*(td+tm)+td", "18*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_019"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(19/(N-1)))/2", "(Wb*(Wt/Wb)^(19/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(19/(N-1)))/2", "(Wb*(Wt/Wb)^(19/(N-1)))/2"
.Zrange "19*(td+tm)", "19*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_019"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(19/(N-1)))/2", "(Wb*(Wt/Wb)^(19/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(19/(N-1)))/2", "(Wb*(Wt/Wb)^(19/(N-1)))/2"
.Zrange "19*(td+tm)+td", "19*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_020"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(20/(N-1)))/2", "(Wb*(Wt/Wb)^(20/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(20/(N-1)))/2", "(Wb*(Wt/Wb)^(20/(N-1)))/2"
.Zrange "20*(td+tm)", "20*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_020"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(20/(N-1)))/2", "(Wb*(Wt/Wb)^(20/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(20/(N-1)))/2", "(Wb*(Wt/Wb)^(20/(N-1)))/2"
.Zrange "20*(td+tm)+td", "20*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_021"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(21/(N-1)))/2", "(Wb*(Wt/Wb)^(21/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(21/(N-1)))/2", "(Wb*(Wt/Wb)^(21/(N-1)))/2"
.Zrange "21*(td+tm)", "21*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_021"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(21/(N-1)))/2", "(Wb*(Wt/Wb)^(21/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(21/(N-1)))/2", "(Wb*(Wt/Wb)^(21/(N-1)))/2"
.Zrange "21*(td+tm)+td", "21*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_022"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(22/(N-1)))/2", "(Wb*(Wt/Wb)^(22/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(22/(N-1)))/2", "(Wb*(Wt/Wb)^(22/(N-1)))/2"
.Zrange "22*(td+tm)", "22*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_022"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(22/(N-1)))/2", "(Wb*(Wt/Wb)^(22/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(22/(N-1)))/2", "(Wb*(Wt/Wb)^(22/(N-1)))/2"
.Zrange "22*(td+tm)+td", "22*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_023"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(23/(N-1)))/2", "(Wb*(Wt/Wb)^(23/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(23/(N-1)))/2", "(Wb*(Wt/Wb)^(23/(N-1)))/2"
.Zrange "23*(td+tm)", "23*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_023"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(23/(N-1)))/2", "(Wb*(Wt/Wb)^(23/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(23/(N-1)))/2", "(Wb*(Wt/Wb)^(23/(N-1)))/2"
.Zrange "23*(td+tm)+td", "23*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_024"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(24/(N-1)))/2", "(Wb*(Wt/Wb)^(24/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(24/(N-1)))/2", "(Wb*(Wt/Wb)^(24/(N-1)))/2"
.Zrange "24*(td+tm)", "24*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_024"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(24/(N-1)))/2", "(Wb*(Wt/Wb)^(24/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(24/(N-1)))/2", "(Wb*(Wt/Wb)^(24/(N-1)))/2"
.Zrange "24*(td+tm)+td", "24*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_025"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(25/(N-1)))/2", "(Wb*(Wt/Wb)^(25/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(25/(N-1)))/2", "(Wb*(Wt/Wb)^(25/(N-1)))/2"
.Zrange "25*(td+tm)", "25*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_025"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(25/(N-1)))/2", "(Wb*(Wt/Wb)^(25/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(25/(N-1)))/2", "(Wb*(Wt/Wb)^(25/(N-1)))/2"
.Zrange "25*(td+tm)+td", "25*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_026"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(26/(N-1)))/2", "(Wb*(Wt/Wb)^(26/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(26/(N-1)))/2", "(Wb*(Wt/Wb)^(26/(N-1)))/2"
.Zrange "26*(td+tm)", "26*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_026"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(26/(N-1)))/2", "(Wb*(Wt/Wb)^(26/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(26/(N-1)))/2", "(Wb*(Wt/Wb)^(26/(N-1)))/2"
.Zrange "26*(td+tm)+td", "26*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_027"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(27/(N-1)))/2", "(Wb*(Wt/Wb)^(27/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(27/(N-1)))/2", "(Wb*(Wt/Wb)^(27/(N-1)))/2"
.Zrange "27*(td+tm)", "27*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_027"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(27/(N-1)))/2", "(Wb*(Wt/Wb)^(27/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(27/(N-1)))/2", "(Wb*(Wt/Wb)^(27/(N-1)))/2"
.Zrange "27*(td+tm)+td", "27*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_028"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(28/(N-1)))/2", "(Wb*(Wt/Wb)^(28/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(28/(N-1)))/2", "(Wb*(Wt/Wb)^(28/(N-1)))/2"
.Zrange "28*(td+tm)", "28*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_028"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(28/(N-1)))/2", "(Wb*(Wt/Wb)^(28/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(28/(N-1)))/2", "(Wb*(Wt/Wb)^(28/(N-1)))/2"
.Zrange "28*(td+tm)+td", "28*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_029"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(29/(N-1)))/2", "(Wb*(Wt/Wb)^(29/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(29/(N-1)))/2", "(Wb*(Wt/Wb)^(29/(N-1)))/2"
.Zrange "29*(td+tm)", "29*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_029"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(29/(N-1)))/2", "(Wb*(Wt/Wb)^(29/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(29/(N-1)))/2", "(Wb*(Wt/Wb)^(29/(N-1)))/2"
.Zrange "29*(td+tm)+td", "29*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_030"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(30/(N-1)))/2", "(Wb*(Wt/Wb)^(30/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(30/(N-1)))/2", "(Wb*(Wt/Wb)^(30/(N-1)))/2"
.Zrange "30*(td+tm)", "30*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_030"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(30/(N-1)))/2", "(Wb*(Wt/Wb)^(30/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(30/(N-1)))/2", "(Wb*(Wt/Wb)^(30/(N-1)))/2"
.Zrange "30*(td+tm)+td", "30*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_031"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(31/(N-1)))/2", "(Wb*(Wt/Wb)^(31/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(31/(N-1)))/2", "(Wb*(Wt/Wb)^(31/(N-1)))/2"
.Zrange "31*(td+tm)", "31*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_031"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(31/(N-1)))/2", "(Wb*(Wt/Wb)^(31/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(31/(N-1)))/2", "(Wb*(Wt/Wb)^(31/(N-1)))/2"
.Zrange "31*(td+tm)+td", "31*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_032"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(32/(N-1)))/2", "(Wb*(Wt/Wb)^(32/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(32/(N-1)))/2", "(Wb*(Wt/Wb)^(32/(N-1)))/2"
.Zrange "32*(td+tm)", "32*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_032"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(32/(N-1)))/2", "(Wb*(Wt/Wb)^(32/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(32/(N-1)))/2", "(Wb*(Wt/Wb)^(32/(N-1)))/2"
.Zrange "32*(td+tm)+td", "32*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_033"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(33/(N-1)))/2", "(Wb*(Wt/Wb)^(33/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(33/(N-1)))/2", "(Wb*(Wt/Wb)^(33/(N-1)))/2"
.Zrange "33*(td+tm)", "33*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_033"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(33/(N-1)))/2", "(Wb*(Wt/Wb)^(33/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(33/(N-1)))/2", "(Wb*(Wt/Wb)^(33/(N-1)))/2"
.Zrange "33*(td+tm)+td", "33*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_034"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(34/(N-1)))/2", "(Wb*(Wt/Wb)^(34/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(34/(N-1)))/2", "(Wb*(Wt/Wb)^(34/(N-1)))/2"
.Zrange "34*(td+tm)", "34*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_034"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(34/(N-1)))/2", "(Wb*(Wt/Wb)^(34/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(34/(N-1)))/2", "(Wb*(Wt/Wb)^(34/(N-1)))/2"
.Zrange "34*(td+tm)+td", "34*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_035"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(35/(N-1)))/2", "(Wb*(Wt/Wb)^(35/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(35/(N-1)))/2", "(Wb*(Wt/Wb)^(35/(N-1)))/2"
.Zrange "35*(td+tm)", "35*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_035"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(35/(N-1)))/2", "(Wb*(Wt/Wb)^(35/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(35/(N-1)))/2", "(Wb*(Wt/Wb)^(35/(N-1)))/2"
.Zrange "35*(td+tm)+td", "35*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_036"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(36/(N-1)))/2", "(Wb*(Wt/Wb)^(36/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(36/(N-1)))/2", "(Wb*(Wt/Wb)^(36/(N-1)))/2"
.Zrange "36*(td+tm)", "36*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_036"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(36/(N-1)))/2", "(Wb*(Wt/Wb)^(36/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(36/(N-1)))/2", "(Wb*(Wt/Wb)^(36/(N-1)))/2"
.Zrange "36*(td+tm)+td", "36*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_037"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(37/(N-1)))/2", "(Wb*(Wt/Wb)^(37/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(37/(N-1)))/2", "(Wb*(Wt/Wb)^(37/(N-1)))/2"
.Zrange "37*(td+tm)", "37*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_037"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(37/(N-1)))/2", "(Wb*(Wt/Wb)^(37/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(37/(N-1)))/2", "(Wb*(Wt/Wb)^(37/(N-1)))/2"
.Zrange "37*(td+tm)+td", "37*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_038"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(38/(N-1)))/2", "(Wb*(Wt/Wb)^(38/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(38/(N-1)))/2", "(Wb*(Wt/Wb)^(38/(N-1)))/2"
.Zrange "38*(td+tm)", "38*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_038"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(38/(N-1)))/2", "(Wb*(Wt/Wb)^(38/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(38/(N-1)))/2", "(Wb*(Wt/Wb)^(38/(N-1)))/2"
.Zrange "38*(td+tm)+td", "38*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_039"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(39/(N-1)))/2", "(Wb*(Wt/Wb)^(39/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(39/(N-1)))/2", "(Wb*(Wt/Wb)^(39/(N-1)))/2"
.Zrange "39*(td+tm)", "39*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_039"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(39/(N-1)))/2", "(Wb*(Wt/Wb)^(39/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(39/(N-1)))/2", "(Wb*(Wt/Wb)^(39/(N-1)))/2"
.Zrange "39*(td+tm)+td", "39*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_040"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(40/(N-1)))/2", "(Wb*(Wt/Wb)^(40/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(40/(N-1)))/2", "(Wb*(Wt/Wb)^(40/(N-1)))/2"
.Zrange "40*(td+tm)", "40*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_040"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(40/(N-1)))/2", "(Wb*(Wt/Wb)^(40/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(40/(N-1)))/2", "(Wb*(Wt/Wb)^(40/(N-1)))/2"
.Zrange "40*(td+tm)+td", "40*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_041"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(41/(N-1)))/2", "(Wb*(Wt/Wb)^(41/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(41/(N-1)))/2", "(Wb*(Wt/Wb)^(41/(N-1)))/2"
.Zrange "41*(td+tm)", "41*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_041"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(41/(N-1)))/2", "(Wb*(Wt/Wb)^(41/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(41/(N-1)))/2", "(Wb*(Wt/Wb)^(41/(N-1)))/2"
.Zrange "41*(td+tm)+td", "41*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_042"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(42/(N-1)))/2", "(Wb*(Wt/Wb)^(42/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(42/(N-1)))/2", "(Wb*(Wt/Wb)^(42/(N-1)))/2"
.Zrange "42*(td+tm)", "42*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_042"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(42/(N-1)))/2", "(Wb*(Wt/Wb)^(42/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(42/(N-1)))/2", "(Wb*(Wt/Wb)^(42/(N-1)))/2"
.Zrange "42*(td+tm)+td", "42*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_043"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(43/(N-1)))/2", "(Wb*(Wt/Wb)^(43/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(43/(N-1)))/2", "(Wb*(Wt/Wb)^(43/(N-1)))/2"
.Zrange "43*(td+tm)", "43*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_043"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(43/(N-1)))/2", "(Wb*(Wt/Wb)^(43/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(43/(N-1)))/2", "(Wb*(Wt/Wb)^(43/(N-1)))/2"
.Zrange "43*(td+tm)+td", "43*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_044"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(44/(N-1)))/2", "(Wb*(Wt/Wb)^(44/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(44/(N-1)))/2", "(Wb*(Wt/Wb)^(44/(N-1)))/2"
.Zrange "44*(td+tm)", "44*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_044"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(44/(N-1)))/2", "(Wb*(Wt/Wb)^(44/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(44/(N-1)))/2", "(Wb*(Wt/Wb)^(44/(N-1)))/2"
.Zrange "44*(td+tm)+td", "44*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_045"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(45/(N-1)))/2", "(Wb*(Wt/Wb)^(45/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(45/(N-1)))/2", "(Wb*(Wt/Wb)^(45/(N-1)))/2"
.Zrange "45*(td+tm)", "45*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_045"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(45/(N-1)))/2", "(Wb*(Wt/Wb)^(45/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(45/(N-1)))/2", "(Wb*(Wt/Wb)^(45/(N-1)))/2"
.Zrange "45*(td+tm)+td", "45*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_046"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(46/(N-1)))/2", "(Wb*(Wt/Wb)^(46/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(46/(N-1)))/2", "(Wb*(Wt/Wb)^(46/(N-1)))/2"
.Zrange "46*(td+tm)", "46*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_046"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(46/(N-1)))/2", "(Wb*(Wt/Wb)^(46/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(46/(N-1)))/2", "(Wb*(Wt/Wb)^(46/(N-1)))/2"
.Zrange "46*(td+tm)+td", "46*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_047"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(47/(N-1)))/2", "(Wb*(Wt/Wb)^(47/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(47/(N-1)))/2", "(Wb*(Wt/Wb)^(47/(N-1)))/2"
.Zrange "47*(td+tm)", "47*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_047"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(47/(N-1)))/2", "(Wb*(Wt/Wb)^(47/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(47/(N-1)))/2", "(Wb*(Wt/Wb)^(47/(N-1)))/2"
.Zrange "47*(td+tm)+td", "47*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_048"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(48/(N-1)))/2", "(Wb*(Wt/Wb)^(48/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(48/(N-1)))/2", "(Wb*(Wt/Wb)^(48/(N-1)))/2"
.Zrange "48*(td+tm)", "48*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_048"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(48/(N-1)))/2", "(Wb*(Wt/Wb)^(48/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(48/(N-1)))/2", "(Wb*(Wt/Wb)^(48/(N-1)))/2"
.Zrange "48*(td+tm)+td", "48*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_049"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(49/(N-1)))/2", "(Wb*(Wt/Wb)^(49/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(49/(N-1)))/2", "(Wb*(Wt/Wb)^(49/(N-1)))/2"
.Zrange "49*(td+tm)", "49*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_049"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(49/(N-1)))/2", "(Wb*(Wt/Wb)^(49/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(49/(N-1)))/2", "(Wb*(Wt/Wb)^(49/(N-1)))/2"
.Zrange "49*(td+tm)+td", "49*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_050"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(50/(N-1)))/2", "(Wb*(Wt/Wb)^(50/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(50/(N-1)))/2", "(Wb*(Wt/Wb)^(50/(N-1)))/2"
.Zrange "50*(td+tm)", "50*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_050"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(50/(N-1)))/2", "(Wb*(Wt/Wb)^(50/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(50/(N-1)))/2", "(Wb*(Wt/Wb)^(50/(N-1)))/2"
.Zrange "50*(td+tm)+td", "50*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_051"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(51/(N-1)))/2", "(Wb*(Wt/Wb)^(51/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(51/(N-1)))/2", "(Wb*(Wt/Wb)^(51/(N-1)))/2"
.Zrange "51*(td+tm)", "51*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_051"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(51/(N-1)))/2", "(Wb*(Wt/Wb)^(51/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(51/(N-1)))/2", "(Wb*(Wt/Wb)^(51/(N-1)))/2"
.Zrange "51*(td+tm)+td", "51*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_052"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(52/(N-1)))/2", "(Wb*(Wt/Wb)^(52/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(52/(N-1)))/2", "(Wb*(Wt/Wb)^(52/(N-1)))/2"
.Zrange "52*(td+tm)", "52*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_052"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(52/(N-1)))/2", "(Wb*(Wt/Wb)^(52/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(52/(N-1)))/2", "(Wb*(Wt/Wb)^(52/(N-1)))/2"
.Zrange "52*(td+tm)+td", "52*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_053"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(53/(N-1)))/2", "(Wb*(Wt/Wb)^(53/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(53/(N-1)))/2", "(Wb*(Wt/Wb)^(53/(N-1)))/2"
.Zrange "53*(td+tm)", "53*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_053"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(53/(N-1)))/2", "(Wb*(Wt/Wb)^(53/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(53/(N-1)))/2", "(Wb*(Wt/Wb)^(53/(N-1)))/2"
.Zrange "53*(td+tm)+td", "53*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_054"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(54/(N-1)))/2", "(Wb*(Wt/Wb)^(54/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(54/(N-1)))/2", "(Wb*(Wt/Wb)^(54/(N-1)))/2"
.Zrange "54*(td+tm)", "54*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_054"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(54/(N-1)))/2", "(Wb*(Wt/Wb)^(54/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(54/(N-1)))/2", "(Wb*(Wt/Wb)^(54/(N-1)))/2"
.Zrange "54*(td+tm)+td", "54*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_055"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(55/(N-1)))/2", "(Wb*(Wt/Wb)^(55/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(55/(N-1)))/2", "(Wb*(Wt/Wb)^(55/(N-1)))/2"
.Zrange "55*(td+tm)", "55*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_055"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(55/(N-1)))/2", "(Wb*(Wt/Wb)^(55/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(55/(N-1)))/2", "(Wb*(Wt/Wb)^(55/(N-1)))/2"
.Zrange "55*(td+tm)+td", "55*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_056"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(56/(N-1)))/2", "(Wb*(Wt/Wb)^(56/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(56/(N-1)))/2", "(Wb*(Wt/Wb)^(56/(N-1)))/2"
.Zrange "56*(td+tm)", "56*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_056"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(56/(N-1)))/2", "(Wb*(Wt/Wb)^(56/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(56/(N-1)))/2", "(Wb*(Wt/Wb)^(56/(N-1)))/2"
.Zrange "56*(td+tm)+td", "56*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_057"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(57/(N-1)))/2", "(Wb*(Wt/Wb)^(57/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(57/(N-1)))/2", "(Wb*(Wt/Wb)^(57/(N-1)))/2"
.Zrange "57*(td+tm)", "57*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_057"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(57/(N-1)))/2", "(Wb*(Wt/Wb)^(57/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(57/(N-1)))/2", "(Wb*(Wt/Wb)^(57/(N-1)))/2"
.Zrange "57*(td+tm)+td", "57*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_058"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(58/(N-1)))/2", "(Wb*(Wt/Wb)^(58/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(58/(N-1)))/2", "(Wb*(Wt/Wb)^(58/(N-1)))/2"
.Zrange "58*(td+tm)", "58*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_058"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(58/(N-1)))/2", "(Wb*(Wt/Wb)^(58/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(58/(N-1)))/2", "(Wb*(Wt/Wb)^(58/(N-1)))/2"
.Zrange "58*(td+tm)+td", "58*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_059"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(59/(N-1)))/2", "(Wb*(Wt/Wb)^(59/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(59/(N-1)))/2", "(Wb*(Wt/Wb)^(59/(N-1)))/2"
.Zrange "59*(td+tm)", "59*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_059"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(59/(N-1)))/2", "(Wb*(Wt/Wb)^(59/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(59/(N-1)))/2", "(Wb*(Wt/Wb)^(59/(N-1)))/2"
.Zrange "59*(td+tm)+td", "59*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_060"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(60/(N-1)))/2", "(Wb*(Wt/Wb)^(60/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(60/(N-1)))/2", "(Wb*(Wt/Wb)^(60/(N-1)))/2"
.Zrange "60*(td+tm)", "60*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_060"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(60/(N-1)))/2", "(Wb*(Wt/Wb)^(60/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(60/(N-1)))/2", "(Wb*(Wt/Wb)^(60/(N-1)))/2"
.Zrange "60*(td+tm)+td", "60*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_061"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(61/(N-1)))/2", "(Wb*(Wt/Wb)^(61/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(61/(N-1)))/2", "(Wb*(Wt/Wb)^(61/(N-1)))/2"
.Zrange "61*(td+tm)", "61*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_061"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(61/(N-1)))/2", "(Wb*(Wt/Wb)^(61/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(61/(N-1)))/2", "(Wb*(Wt/Wb)^(61/(N-1)))/2"
.Zrange "61*(td+tm)+td", "61*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_062"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(62/(N-1)))/2", "(Wb*(Wt/Wb)^(62/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(62/(N-1)))/2", "(Wb*(Wt/Wb)^(62/(N-1)))/2"
.Zrange "62*(td+tm)", "62*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_062"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(62/(N-1)))/2", "(Wb*(Wt/Wb)^(62/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(62/(N-1)))/2", "(Wb*(Wt/Wb)^(62/(N-1)))/2"
.Zrange "62*(td+tm)+td", "62*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_063"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(63/(N-1)))/2", "(Wb*(Wt/Wb)^(63/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(63/(N-1)))/2", "(Wb*(Wt/Wb)^(63/(N-1)))/2"
.Zrange "63*(td+tm)", "63*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_063"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(63/(N-1)))/2", "(Wb*(Wt/Wb)^(63/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(63/(N-1)))/2", "(Wb*(Wt/Wb)^(63/(N-1)))/2"
.Zrange "63*(td+tm)+td", "63*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_064"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(64/(N-1)))/2", "(Wb*(Wt/Wb)^(64/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(64/(N-1)))/2", "(Wb*(Wt/Wb)^(64/(N-1)))/2"
.Zrange "64*(td+tm)", "64*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_064"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(64/(N-1)))/2", "(Wb*(Wt/Wb)^(64/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(64/(N-1)))/2", "(Wb*(Wt/Wb)^(64/(N-1)))/2"
.Zrange "64*(td+tm)+td", "64*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_065"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(65/(N-1)))/2", "(Wb*(Wt/Wb)^(65/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(65/(N-1)))/2", "(Wb*(Wt/Wb)^(65/(N-1)))/2"
.Zrange "65*(td+tm)", "65*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_065"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(65/(N-1)))/2", "(Wb*(Wt/Wb)^(65/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(65/(N-1)))/2", "(Wb*(Wt/Wb)^(65/(N-1)))/2"
.Zrange "65*(td+tm)+td", "65*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_066"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(66/(N-1)))/2", "(Wb*(Wt/Wb)^(66/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(66/(N-1)))/2", "(Wb*(Wt/Wb)^(66/(N-1)))/2"
.Zrange "66*(td+tm)", "66*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_066"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(66/(N-1)))/2", "(Wb*(Wt/Wb)^(66/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(66/(N-1)))/2", "(Wb*(Wt/Wb)^(66/(N-1)))/2"
.Zrange "66*(td+tm)+td", "66*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_067"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(67/(N-1)))/2", "(Wb*(Wt/Wb)^(67/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(67/(N-1)))/2", "(Wb*(Wt/Wb)^(67/(N-1)))/2"
.Zrange "67*(td+tm)", "67*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_067"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(67/(N-1)))/2", "(Wb*(Wt/Wb)^(67/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(67/(N-1)))/2", "(Wb*(Wt/Wb)^(67/(N-1)))/2"
.Zrange "67*(td+tm)+td", "67*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_068"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(68/(N-1)))/2", "(Wb*(Wt/Wb)^(68/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(68/(N-1)))/2", "(Wb*(Wt/Wb)^(68/(N-1)))/2"
.Zrange "68*(td+tm)", "68*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_068"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(68/(N-1)))/2", "(Wb*(Wt/Wb)^(68/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(68/(N-1)))/2", "(Wb*(Wt/Wb)^(68/(N-1)))/2"
.Zrange "68*(td+tm)+td", "68*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_069"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(69/(N-1)))/2", "(Wb*(Wt/Wb)^(69/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(69/(N-1)))/2", "(Wb*(Wt/Wb)^(69/(N-1)))/2"
.Zrange "69*(td+tm)", "69*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_069"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(69/(N-1)))/2", "(Wb*(Wt/Wb)^(69/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(69/(N-1)))/2", "(Wb*(Wt/Wb)^(69/(N-1)))/2"
.Zrange "69*(td+tm)+td", "69*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_070"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(70/(N-1)))/2", "(Wb*(Wt/Wb)^(70/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(70/(N-1)))/2", "(Wb*(Wt/Wb)^(70/(N-1)))/2"
.Zrange "70*(td+tm)", "70*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_070"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(70/(N-1)))/2", "(Wb*(Wt/Wb)^(70/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(70/(N-1)))/2", "(Wb*(Wt/Wb)^(70/(N-1)))/2"
.Zrange "70*(td+tm)+td", "70*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_071"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(71/(N-1)))/2", "(Wb*(Wt/Wb)^(71/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(71/(N-1)))/2", "(Wb*(Wt/Wb)^(71/(N-1)))/2"
.Zrange "71*(td+tm)", "71*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_071"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(71/(N-1)))/2", "(Wb*(Wt/Wb)^(71/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(71/(N-1)))/2", "(Wb*(Wt/Wb)^(71/(N-1)))/2"
.Zrange "71*(td+tm)+td", "71*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_072"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(72/(N-1)))/2", "(Wb*(Wt/Wb)^(72/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(72/(N-1)))/2", "(Wb*(Wt/Wb)^(72/(N-1)))/2"
.Zrange "72*(td+tm)", "72*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_072"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(72/(N-1)))/2", "(Wb*(Wt/Wb)^(72/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(72/(N-1)))/2", "(Wb*(Wt/Wb)^(72/(N-1)))/2"
.Zrange "72*(td+tm)+td", "72*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_073"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(73/(N-1)))/2", "(Wb*(Wt/Wb)^(73/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(73/(N-1)))/2", "(Wb*(Wt/Wb)^(73/(N-1)))/2"
.Zrange "73*(td+tm)", "73*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_073"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(73/(N-1)))/2", "(Wb*(Wt/Wb)^(73/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(73/(N-1)))/2", "(Wb*(Wt/Wb)^(73/(N-1)))/2"
.Zrange "73*(td+tm)+td", "73*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_074"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(74/(N-1)))/2", "(Wb*(Wt/Wb)^(74/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(74/(N-1)))/2", "(Wb*(Wt/Wb)^(74/(N-1)))/2"
.Zrange "74*(td+tm)", "74*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_074"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(74/(N-1)))/2", "(Wb*(Wt/Wb)^(74/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(74/(N-1)))/2", "(Wb*(Wt/Wb)^(74/(N-1)))/2"
.Zrange "74*(td+tm)+td", "74*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_075"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(75/(N-1)))/2", "(Wb*(Wt/Wb)^(75/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(75/(N-1)))/2", "(Wb*(Wt/Wb)^(75/(N-1)))/2"
.Zrange "75*(td+tm)", "75*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_075"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(75/(N-1)))/2", "(Wb*(Wt/Wb)^(75/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(75/(N-1)))/2", "(Wb*(Wt/Wb)^(75/(N-1)))/2"
.Zrange "75*(td+tm)+td", "75*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_076"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(76/(N-1)))/2", "(Wb*(Wt/Wb)^(76/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(76/(N-1)))/2", "(Wb*(Wt/Wb)^(76/(N-1)))/2"
.Zrange "76*(td+tm)", "76*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_076"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(76/(N-1)))/2", "(Wb*(Wt/Wb)^(76/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(76/(N-1)))/2", "(Wb*(Wt/Wb)^(76/(N-1)))/2"
.Zrange "76*(td+tm)+td", "76*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_077"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(77/(N-1)))/2", "(Wb*(Wt/Wb)^(77/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(77/(N-1)))/2", "(Wb*(Wt/Wb)^(77/(N-1)))/2"
.Zrange "77*(td+tm)", "77*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_077"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(77/(N-1)))/2", "(Wb*(Wt/Wb)^(77/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(77/(N-1)))/2", "(Wb*(Wt/Wb)^(77/(N-1)))/2"
.Zrange "77*(td+tm)+td", "77*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_078"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(78/(N-1)))/2", "(Wb*(Wt/Wb)^(78/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(78/(N-1)))/2", "(Wb*(Wt/Wb)^(78/(N-1)))/2"
.Zrange "78*(td+tm)", "78*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_078"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(78/(N-1)))/2", "(Wb*(Wt/Wb)^(78/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(78/(N-1)))/2", "(Wb*(Wt/Wb)^(78/(N-1)))/2"
.Zrange "78*(td+tm)+td", "78*(td+tm)+td+tm"
.Create 
End With
With Brick
.Reset 
.Name "d_079"
.Component "pyramid"
.Material "Dielectric"
.Xrange "-(Wb*(Wt/Wb)^(79/(N-1)))/2", "(Wb*(Wt/Wb)^(79/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(79/(N-1)))/2", "(Wb*(Wt/Wb)^(79/(N-1)))/2"
.Zrange "79*(td+tm)", "79*(td+tm)+td"
.Create 
End With
With Brick
.Reset 
.Name "cu_079"
.Component "pyramid"
.Material "Copper"
.Xrange "-(Wb*(Wt/Wb)^(79/(N-1)))/2", "(Wb*(Wt/Wb)^(79/(N-1)))/2"
.Yrange "-(Wb*(Wt/Wb)^(79/(N-1)))/2", "(Wb*(Wt/Wb)^(79/(N-1)))/2"
.Zrange "79*(td+tm)+td", "79*(td+tm)+td+tm"
.Create 
End With

'@ 04_boundary

'[VERSION]2023.4|32.0.1|20230426[/VERSION]
With Background
.Type "Normal"
.Epsilon "1"
.Mue "1"
.XminSpace "0"
.XmaxSpace "0"
.YminSpace "0"
.YmaxSpace "0"
.ZminSpace "3"
.ZmaxSpace "8"
End With
With Boundary
.Xmin "unit cell"
.Xmax "unit cell"
.Ymin "unit cell"
.Ymax "unit cell"
.Zmin "open"
.Zmax "open"
.Xsymmetry "none"
.Ysymmetry "none"
.Zsymmetry "none"
.SetPeriodicBoundaryAngles "0", "0"
.UnitCellFitToBoundingBox "True"
.UnitCellAngle "90"
End With

'@ 05_ports

'[VERSION]2023.4|32.0.1|20230426[/VERSION]
With FloquetPort
.Reset
.SetDialogFrequency "40"
.SetDialogTheta "0"
.SetDialogPhi "0"
.Port "Zmin"
.SetCustomizedListFlag "True"
.SetNumberOfModesConsidered "50"
.AddMode "TE", "0", "0"
.AddMode "TM", "0", "0"
.AddMode "TE", "-1", "0"
.AddMode "TM", "-1", "0"
.AddMode "TE", "0", "-1"
.AddMode "TM", "0", "-1"
.AddMode "TE", "0", "1"
.AddMode "TM", "0", "1"
.AddMode "TE", "1", "0"
.AddMode "TM", "1", "0"
.AddMode "TE", "-1", "-1"
.AddMode "TM", "-1", "-1"
.AddMode "TE", "-1", "1"
.AddMode "TM", "-1", "1"
.AddMode "TE", "1", "-1"
.AddMode "TM", "1", "-1"
.AddMode "TE", "1", "1"
.AddMode "TM", "1", "1"
.AddMode "TE", "-2", "0"
.AddMode "TM", "-2", "0"
.AddMode "TE", "0", "-2"
.AddMode "TM", "0", "-2"
.AddMode "TE", "0", "2"
.AddMode "TM", "0", "2"
.AddMode "TE", "2", "0"
.AddMode "TM", "2", "0"
.AddMode "TE", "-2", "-1"
.AddMode "TM", "-2", "-1"
.AddMode "TE", "-2", "1"
.AddMode "TM", "-2", "1"
.AddMode "TE", "-1", "-2"
.AddMode "TM", "-1", "-2"
.AddMode "TE", "-1", "2"
.AddMode "TM", "-1", "2"
.AddMode "TE", "1", "-2"
.AddMode "TM", "1", "-2"
.AddMode "TE", "1", "2"
.AddMode "TM", "1", "2"
.AddMode "TE", "2", "-1"
.AddMode "TM", "2", "-1"
.AddMode "TE", "2", "1"
.AddMode "TM", "2", "1"
.AddMode "TE", "-2", "-2"
.AddMode "TM", "-2", "-2"
.AddMode "TE", "-2", "2"
.AddMode "TM", "-2", "2"
.AddMode "TE", "2", "-2"
.AddMode "TM", "2", "-2"
.AddMode "TE", "2", "2"
.AddMode "TM", "2", "2"
.Port "Zmax"
.SetCustomizedListFlag "True"
.SetNumberOfModesConsidered "50"
.AddMode "TE", "0", "0"
.AddMode "TM", "0", "0"
.AddMode "TE", "-1", "0"
.AddMode "TM", "-1", "0"
.AddMode "TE", "0", "-1"
.AddMode "TM", "0", "-1"
.AddMode "TE", "0", "1"
.AddMode "TM", "0", "1"
.AddMode "TE", "1", "0"
.AddMode "TM", "1", "0"
.AddMode "TE", "-1", "-1"
.AddMode "TM", "-1", "-1"
.AddMode "TE", "-1", "1"
.AddMode "TM", "-1", "1"
.AddMode "TE", "1", "-1"
.AddMode "TM", "1", "-1"
.AddMode "TE", "1", "1"
.AddMode "TM", "1", "1"
.AddMode "TE", "-2", "0"
.AddMode "TM", "-2", "0"
.AddMode "TE", "0", "-2"
.AddMode "TM", "0", "-2"
.AddMode "TE", "0", "2"
.AddMode "TM", "0", "2"
.AddMode "TE", "2", "0"
.AddMode "TM", "2", "0"
.AddMode "TE", "-2", "-1"
.AddMode "TM", "-2", "-1"
.AddMode "TE", "-2", "1"
.AddMode "TM", "-2", "1"
.AddMode "TE", "-1", "-2"
.AddMode "TM", "-1", "-2"
.AddMode "TE", "-1", "2"
.AddMode "TM", "-1", "2"
.AddMode "TE", "1", "-2"
.AddMode "TM", "1", "-2"
.AddMode "TE", "1", "2"
.AddMode "TM", "1", "2"
.AddMode "TE", "2", "-1"
.AddMode "TM", "2", "-1"
.AddMode "TE", "2", "1"
.AddMode "TM", "2", "1"
.AddMode "TE", "-2", "-2"
.AddMode "TM", "-2", "-2"
.AddMode "TE", "-2", "2"
.AddMode "TM", "-2", "2"
.AddMode "TE", "2", "-2"
.AddMode "TM", "2", "-2"
.AddMode "TE", "2", "2"
.AddMode "TM", "2", "2"
End With

'@ 06_solver

'[VERSION]2023.4|32.0.1|20230426[/VERSION]
With FDSolver
.Reset 
.SetMethod "Tetrahedral", "General Purpose"
.OrderTet "Second"
.Type "Direct"
.Stimulation "List", "List"
.ResetExcitationList 
.AddToExcitationList "Zmax", "TE(0,0)"
.AccuracyTet "1e-5"
.MeshAdaptionTet "True"
.FrequencySamples "220"
.SetNumberOfResultDataSamples "3501"
.SetResultDataSamplingMode "Frequency (linear)"
.UseParallelization "True"
.MaxCPUs "8"
.SetStopSweepIfCriterionMet "True"
.SetSweepThreshold "S-Parameters", "0.001"
.SweepErrorChecks "3"
.SweepMinimumSamples "15"
End With
With MeshAdaption3D
.SetType "HighFrequencyTet"
.MinPasses "4"
.MaxPasses "7"
.MaxDeltaS "0.003"
.NumberOfDeltaSChecks "2"
.RemoveAllUserDefinedStopCriteria 
.AddStopCriterion "All S-Parameters", "0.003", "2", "True"
End With

'@ 07_critical_stability_samples

'[VERSION]2023.4|32.0.1|20230426[/VERSION]
With FDSolver
.SetMethod "", "Discrete samples only"
.ResetSampleIntervals "all"
.AddSampleInterval "12.23", "12.23", "1", "Single", "True"
End With

