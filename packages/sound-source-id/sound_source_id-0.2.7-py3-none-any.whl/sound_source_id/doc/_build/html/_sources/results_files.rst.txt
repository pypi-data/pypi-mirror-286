.. _sec-results_files:

*************
Results files
*************

The main results file is a comma-separated values (CSV) file. Note that the CSV separator is not necessarily a comma, and can be changed in the ``General`` Preferences tab accessible by clicking ``Edit``, and then ``Preferences``. The main results file contains a row for each trial with the following fields:

  - `listener`: the listener identifier
  - `condition`: the experimental condition
  - `block`: the block number
  - `trial`: the trial number
  - `azimuth_angle`: the stimulus azimuth angle, as specified in the parameters file
  - `elevation_angle`: the stimulus elevation angle, as specified in the parameters file
  - `response_azimuth`: the response azimuth angle 
  - `response_elevation`: the response elevation angle
  - `azimuth_error`: the signed azimuth angle error
  - `elevation_error`: the signed elevation angle error
  - `azimuth_angle_remapped`: the stimulus azimuth angle remapped to the 0-360° range
  - `response_azimuth_remapped`: the response azimuth angle remapped to the 0-360° range
  - `azimuth_angle_flip`: the stimulus azimuth angle obtained after `flipping` (reflecting/mirroring) the stimulus positions from the rear to the front
  - `response_azimuth_flip`: the response azimuth angle obtained after `flipping` (reflecting/mirroring) the stimulus positions from the rear to the front
  - `azimuth_error_flip`: the azimuth error calculated from stimulus and response angles flipped to the front (this is one way to calculate errors while ignoring front-back confusions)
  - `front-back`: [``0``, ``1``] 1 if the listener made a front-back confusion, 0 otherwise
  - `sound_file`: the sound file used for the trial
  - `base_level` the base level, in dB SPL, for the trial
  - `rove`: the level rove range for the trial
  - `actual_level`: the actual level at which the stimulus was played
  - `date`: the date 
  - `time`: the time

``sound_source_id`` additionally outputs summary files for the all the trials, as well as by experimental condition and/or by block if multiple conditions/blocks are present (and by block x condition). For each of these subdivisions of the results, one summary file gives root-mean-square (RMS) azimuth and elevation errors, and the other front-back error proportions. The RMS error files contain the following fields:

  - `listener`: the listener's identifier
  - `rms_azimuth_err`: the RMS azimuth error
  - `rms_elevation_err`: the RMS elevation error
  - `rms_azimuth_err_flip`: the RMS azimuth error calculated after both stimuli and responses positions have been flipped from the rear to the front (this is one way to compute RMS errors while ignoring front-back errors)
  - `azr_rms_err_no_FB`: the RMS azimuth error calculated after excluding trials with front-back errors (this is another way to compute RMS errors while ignoring front-back errors). Front-back errors are defined here as cases in which the RMS error is reduced after flipping both stimuli and responses positions to the front

The front-back error files contain the following fields:

  - `listener`: the listener's identifier
  - `front_back`: the proportion of front-back errors
  
