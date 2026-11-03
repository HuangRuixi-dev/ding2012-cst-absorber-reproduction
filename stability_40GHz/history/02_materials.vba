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