With Material
.Reset 
.Name "Dielectric_design"
.Type "Normal"
.Epsilon "eps_r"
.Mue "1"
.TanD "loss_tan"
.TanDFreq "10"
.TanDGiven "True"
.TanDModel "ConstTanD"
.Colour "0.5", "0.2", "0.6"
.Create 
End With
With Material
.Reset 
.Name "Copper_design"
.Type "Lossy metal"
.Epsilon "1"
.Mue "1"
.Kappa "5e7"
.Colour "0.9", "0.7", "0.2"
.Create 
End With