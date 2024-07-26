.. _sec-experiment_setup:

***************
Parameters file
***************

The settings for a test are stored in a parameters file, which is a plain text file. An example parameters file for a setup with physical speakers is shown below::

  mode: speakers
  azimuths : -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70
  elevs: 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
  labels : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
  channels : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
  n_chan : 15
  n_blocks : 1
  stim_list_file : stim_list.csv
  randomize : true
  demo_stim : pink_noises/noise1.wav
  demo_stim_lev : 65


this is what each field indicates:

  - `mode`: [``speakers``, ``earphones``], whether spatialization will be achieved by presenting the stimuli through a physical array of speakers, or virtually through earphones
  - `azimuths`: the azimuth angles (in degrees) at which the sounds are presented. Note that a 0° angle indicates straight ahead, a 90° angle is to the right, and a -90° angle to the left
  - `elevs`: the elevation angles (in degrees) at which the sounds are presented; (0°: median plane front, 90°: up, 180°: median plane back, 270: down°). This field can be omitted if all of the elevation angles are at 0°
  - `labels`: a label for each of the angles, this can be a number or a letter (e.g., a, b, c, etc...)
  - `channels`: the channel of the soundcard that will be used to present a sound at the corresponding azimuth/elevation coordinate
  - `n_chan`: the total number of channels for the setup
  - `n_blocks`: the number of blocks, that is, how many times the test will be repeated
  - `stim_list_file`: the path (absolute or relative) to the file containing the stimulation list (see below)
  - `randomize`: if `true` the stim_list_file will be shuffled before the repetition of each block
  - `demo_stim`: the path to the WAV file to be used for the demo
  - `demo_stim_lev`: the sound level (in dB SPL) to be used for the demo

Below is an example parameter file for a setup with virtual spatial presentation through earphones::

  mode: earphones
  azimuths : -70, -60, -50, -40, -30, -20, -10, 0, 10, 20, 30, 40, 50, 60, 70
  labels : 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15
  n_blocks : 1
  stim_list_file : stim_list.csv
  randomize : true
  demo_stim : pink_noises/noise1.wav
  demo_stim_lev : 65
  sofa_file_path: /media/ntfsShared/archives/auditory/Materials/KU100_Far_Field/HRIR_CIRC360.sofa
  sofa_az_coords: anticlockwise

many of the fields in the parameter file above are the same as for a parameter file for a setup with physical speakers. The following additional fields are needed in a parameters file for virtual spatial presentation through earphones:
  - `sofa_file_path`: the path (absolute or relative) to the SOFA file containing the HRTF to be used for spatialization
  - `sofa_az_coords`: [``anticlockwise``, ``clockwise``], whether the azimuth coordinates of the SOFA file are specified in a clockwise(0: front, 90: right, 180: back; 270: left), or anti-clockwise (0: front, 90: left, 180: back; 270: right) arrangement
    
In a parameter file for a setup with virtual spatial presentation through earphones the `channels` and `n_chan` fields are not needed, and will be ignored if present. 



    
****************
Stimulation file
****************

Stimulation files specify the stimuli that will be played on each trial of the test. Figure :ref:`fig-stim_file` shows an example stimulation file.

.. _fig-stim_file:

.. figure:: Figures/stim_file.png
   :scale: 80%
   :alt: Example stimulation file

   Example stimulation file.

Each row of the file represents a trial. Stimulation files contain the following columns:

  - `az_angle`: the azimuth angle at which the sound will be presented (if in mode `speakers`, stimuli will be sent to the corresponding soundcard channel as specified in the parameters file)
  - `elev_angle`: the elevation angle at which the sound will be presented (if in mode `speakers`, stimuli will be sent to the corresponding soundcard channel as specified in the parameters file)
  - `sound_file`: the path (relative or absolute) to the WAV file to be played
  - `condition`: an optional label specifying the experimental condition
  - `level`: the `base` sound level (in dB SPL) at which the sound will be presented (this assumes that `sound_source_id` has been correctly calibrated)
  - `roving`: a level rove, the actual sound level will be equal to the base level plus a value drawn from a random uniform distribution between +/- the roving level
  - `feedback`: if `true`, feedback will be given to the listener at the end of each trial
