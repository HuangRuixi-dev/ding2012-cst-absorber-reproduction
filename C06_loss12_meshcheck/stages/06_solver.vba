With FDSolver
.Reset 
.SetMethod "Tetrahedral", "General Purpose"
.OrderTet "Second"
.Stimulation "List", "List"
.ResetExcitationList 
.AddToExcitationList "Zmax", "TE(0,0)"
.AccuracyTet "1e-5"
.MeshAdaptionTet "True"
.FrequencySamples "160"
.SetNumberOfResultDataSamples "2601"
.SetResultDataSamplingMode "Frequency (linear)"
.UseParallelization "True"
.MaxCPUs "8"
End With
With FDSolver
.SetStopSweepIfCriterionMet "True"
.SetSweepThreshold "S-Parameters", "0.001"
.SweepErrorChecks "3"
.SweepMinimumSamples "10"
End With

With MeshAdaption3D
.SetType "HighFrequencyTet"
.MinPasses "4"
.MaxPasses "8"
.MaxDeltaS "0.003"
.NumberOfDeltaSChecks "2"
.RemoveAllUserDefinedStopCriteria
.AddStopCriterion "All S-Parameters", "0.003", "2", "True"
End With
