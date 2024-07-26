****************************
``sound_source_id``
****************************

``sound_source_id`` is a program for testing sound localization. The interface is shown in Figure :ref:`fig-sound_source_id_screenshot`.

.. _fig-sound_source_id_screenshot:

.. figure:: Figures/sound_source_id_screenshot.png
   :scale: 50%
   :alt: Screenshot of the ``sound_source_id`` interface

   Screenshot of the ``sound_source_id`` interface

   ``sound_source_id`` supports presenting sounds through a physical array of speakers laid out in a circular (or spherical, if multiple elevations are used) layout, or through earphones. In the latter case, spazialization is achieved by convolving the stimuli with an head-related transfer function (which must be provided by the used through a SOFA file). 
