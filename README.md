# README

DeepEYE is a graphical interface designed to perform visual validation
of putative CNVs.

It is available in a docker singularity container at:
<https://hub.docker.com/r/sinomem/docker_cnv_protocol>

To run it using Singularity

```
singularity pull ibpcnv.simg docker://sinomem/docker_cnv_protocol:latest

singularity exec ibpcnv.simg python3 /opt/eyeCNV/visualizer.py \
    $workingdir putative_cnvs.txt loci.txt samples_list.txt
```
