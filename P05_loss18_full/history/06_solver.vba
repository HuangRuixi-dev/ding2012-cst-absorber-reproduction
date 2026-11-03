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
.SetSweepThreshold "S-Parameters", "0.003"
.SweepErrorChecks "3"
.SweepMinimumSamples "15"
End With
With MeshAdaption3D
.SetType "HighFrequencyTet"
.MinPasses "3"
.MaxPasses "7"
.MaxDeltaS "0.006"
.NumberOfDeltaSChecks "2"
.RemoveAllUserDefinedStopCriteria 
.AddStopCriterion "All S-Parameters", "0.006", "2", "True"
End With