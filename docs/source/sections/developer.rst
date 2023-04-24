Developer's Guide
=================

Adding a dataset
----------------

- Create dataset subclass:

  - *Selecting adequate inheritance*.

    - CDF files should inherit from *CdfData*, FITS files, from *FitsData*,
      binary files from *BinData*.
    - Datasets with varying / fixed spectral sampling should use the
      *VaryingFrequencies* / *FixedFrequencies* mixin, respectively. For
      times series (without a spectral axis), the *RecordsOnly* mixin
      shall be used.

  - *Defining the required attributes and methods*.

    - The dataset name is defined as a class attribute.
    - Each dataset class must have a *.times* property, providing the
      record or sweep time stamps. It must return an astropy.time.Time
      object.
    - Each dataset class with a spectral axis must have a *.frequencies*
      property, providing the sweep spectral axis. It must return an
      astropy.units.Quantity object (for fixed frequency datasets), or a
      list of astropy.units.Quantity objects (for varying frequency
      datasets).
    - Each dataset class shall implement a *.as_xarray()* method returning a
      dictionary, dataset parameter names as keys, and xarray.DataArray as
      values.
    - Each dataset class shall implement a *.quicklook()* method.
    - Each dataset class shall implement a *.epncore* property providing a
      dictionary of (key, values) consistent with the VESPA/EPNcore metadata
      standard.


  - *Setup the dataset resolver engine*.

    - For CDF files, the dataset name must be the value of the *Logical_source*
      global attribute. If it is not possible, the *maser.data.base.CdfData.get_dataset*
      classmethod shall be updated.
    - For FITS files, the mapping is done using the *INSTRUME* and *TELESCOP*
      primary header metadata. The *maser.data.base.FitsData.get_dataset* must
      be updated to implement the mapping.
    - For binary files, the mapping is done using a *regex* pattern on the file
      name. The *dataset_filename_regex.json* file contains the mapping between
      the dataset name and the *regex* pattern to be matched. The file shall be
      updated to include the new mapping.

- Update tests

  - For each new dataset class, a test module shall be implemented, with a goal
    code coverage of 100%.
  - The test files for the dataset shall be submitted to the MASER team, or
    accessible publicly. The test files must be registered in the *collection.json*
    file. The *fixture.py* file shall be updated if the data files are to be
    downloaded from a different location than the MASER data repository. Tests
    file shall not be included in the git repository.
