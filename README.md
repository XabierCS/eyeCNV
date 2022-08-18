# README

DeepEYE is a graphical interface designed to perform visual validation
of putative CNVs.


It is available in a docker container at:
<https://hub.docker.com/r/sinomem/docker_cnv_protocol>

To run it using Singularity

```
cd /path/to/working/directory

singularity pull ibpcnv.simg docker://sinomem/docker_cnv_protocol:latest

git clone https://github.com/XabierCS/eyeCNV.git

singularity exec ibpcnv.simg python3 /opt/eyeCNV/visualizer.py \
    path/to/eyeCNV/toy_data/ put_cnvs.txt loci.txt samples_list.txt GC_YES
```


It can also be run in a `conda` or `venv` environment, given the following dependecies:

- python 3.6
- pandas
- numpy
- Pyqt5==5.12.3
- pyqtgraph==0.12.3
