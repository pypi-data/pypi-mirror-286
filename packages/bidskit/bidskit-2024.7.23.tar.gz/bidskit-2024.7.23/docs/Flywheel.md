## Flywheel Export Support

Flywheel allows export of DICOM data from a project, subject or session from the web interface.  
The most common download format is as a ZIP archive with the following internal structure:

```
flywheel or scitran
└── odoherty
    └── OLEL
        └── JOD_OLEL_031
            └── 1
                ├── anat-MEGRE
                │   └── 1.3.12.2.1107.5.2.43.167050.2023010410414566046477344.0.0.0.dicom.zip
                ├── anat-MEGRE RMS
                │   └── 1.3.12.2.1107.5.2.43.167050.2023010410483321035277560.0.0.0.dicom.zip
                ├── anat-MEGRE RMS_1
                │   └── 1.3.12.2.1107.5.2.43.167050.2023010410483321090177563.0.0.0.dicom.zip
                ├── anat-MEGRE_1
                │   └── 1.3.12.2.1107.5.2.43.167050.2023010410483317378977552.0.0.0.dicom.zip
                ├── anat-gre_acq-localizer
                │   └── 1.3.12.2.1107.5.2.43.167050.2023010409440829026077292.0.0.0.dicom.zip
                ├── fmap-epi_acq-olel_dir-AP_run-1
                │   └── fmap-epi_acq-olel_dir-AP_run-1.dcm
                ├── fmap-epi_acq-olel_dir-PA_run-1
                │   └── fmap-epi_acq-olel_dir-PA_run-1.dcm
                ├── func-bold_task-olel_run-1
                │   └── 1.3.12.2.1107.5.2.43.167050.202301040948137858777630.0.0.0.dicom.zip
                ├── func-bold_task-olel_run-1_PhysioLog
                │   └── func-bold_task-olel_run-1_PhysioLog.dcm
                └── func-bold_task-olel_run-1_SBRef
                    └── func-bold_task-olel_run-1_SBRef.dcm

```
Single DICOM series are uncompressed, but series containing more than one DICOM image file are ZIP compressed.

## BIDSKIT curation of Flywheel DICOM zip archives

1. Create a BIDS dataset directory and move or copy all Flywheel DICOM zip archives to this directory
2. Run bidskit from this directory with the --flywheel command line option to unpack the tarballs into the `sourcedata`
folder and build the template BIDS files and folders (Phase 1)
```
$ bidskit --flywheel <other command line arguments>
```
3. Edit `code/Protocol_Translator.json` manually or use the `--auto` option to autofill the translator file
4. Run bidskit again (Phase 2) without the `--flywheel` option to complete the curation
```
$ bidskit <other command line arguments>
```
5. Delete or move the original Flywheel zip archives