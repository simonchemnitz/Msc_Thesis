from new_dataformat import format_all_metric_files, format_all_observer_files, merge_metric_and_observers


file_dir = "/users/simon/documents/GitHub/Msc_Thesis/HC_Analysis/Files_ig/"
metric_dir = file_dir + "Metric_Results/"
obs_dir  =   file_dir + "Observer_Results/"

out_dir = file_dir + "Merge_Output/"


#Format metric files
reference_date = "_11_01_"
reference_name = "Values"
format_all_metric_files(metric_dir, reference_date, reference_name, save_subfiles = False, out_dir = out_dir, save_file = "")

#Format observer files
format_all_observer_files(obs_dir, save_subfiles = False, out_dir = out_dir, save_file="")

#Merge observer and metric scores
merge_metric_and_observers(out_dir + "All_metric.csv", out_dir+"All_observer.csv", out_dir)