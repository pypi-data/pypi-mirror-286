import pandas as pd
import numpy as np


def read_pure_inference_output(filepath_='/Users/sishitan/Documents/Scripts/qusi_project/qusi/inferences'
                                         '/results_ts0_550k.csv') -> pd.DataFrame:
    """
    Read the inference output as a Pandas data frame
    :return: The inference output
    """
    df = pd.read_csv(filepath_)
    return df


def read_inference_with_tags_and_labels(filepath_='/Users/sishitan/Documents/Scripts/qusi_project/qusi/inferences'
                                        '/results_ts0_550k_with_tags.csv') -> pd.DataFrame:
    """
    Read the inference output with Sumi tags and labels as a Pandas data frame
    :param filepath_:
    :return:
    """
    df = pd.read_csv(filepath_, index_col=False, na_values=(), keep_default_na=False)
    return df


def meaning_of_sumi_tags(tag):
    if tag == 'v':
        meaning = 'Variable star'
    elif tag == 'n':
        meaning = 'Novalike objects'
    elif tag == 'nr':
        meaning = 'CV with repeating flares'
    elif tag == 'm':
        meaning = 'Moving objects'
    elif tag == 'j':
        meaning = 'Junk'
    elif tag == 'no_tag':
        meaning = 'No tag'
    elif tag == '':
        meaning = 'No tag'
    elif tag == np.nan:
        meaning = 'No tag'
    elif tag == 'c':
        meaning = 'Single-lens candidate'
    elif tag == 'cf':
        meaning = 'Single-lens candidate with finite source'
    elif tag == 'cp':
        meaning = 'Single-lens candidate with parallax'
    elif tag == 'cw':
        meaning = 'Weak candidate'
    elif tag == 'cs':
        meaning = 'Short event single-lens candidate'
    elif tag == 'cb':
        meaning = 'Binary lens candidate'
    else:
        meaning = np.nan
    return meaning


def read_sumi_nine_year_label(
        filepath_="/Users/sishitan/Documents/Scripts/qusi_project/qusi/data/moa_microlensing_550k/candlist_2023Oct12.txt") -> pd.DataFrame:
    """
    Reads Takahiro Sumi's 9-year events table as a Pandas data frame
    :param path: The path to the events table file.
    :return: The data frame.
    """
    column_names = ['field', 'band', 'chip', 'subframe', 'ID',
                    'sumi_tag',
                    'x', 'y',
                    'tag06_07', 'separation06_07', 'ID06_07',
                    'x06_07', 'y06_07',
                    'tag_alert', 'separation_alert', 'name_alert',
                    'x_alert', 'y_alert',
                    'tag_extra_alert', 'separation_extra_alert', 'name_extra_alert',
                    'x_extra_alert', 'y_extra_alert',
                    'tag_extra_alert2', 'separation_extra_alert2', 'name_extra_alert2',
                    'x_extra_alert2', 'y_extra_alert2',
                    'tag_extra_alert3', 'separation_extra_alert3', 'name_extra_alert3',
                    'x_extra_alert3', 'y_extra_alert3'
                    ]
    column_types = {'field': np.str_, 'band': np.str_, 'chip': np.int_, 'subframe': np.int_, 'ID': np.int_,
                    'sumi_tag': np.str_,
                    'x': np.float64, 'y': np.float64,
                    'tag06_07': np.str_, 'separation06_07': np.float64, 'ID06_07': 'Int64',
                    'x06_07': np.float64, 'y06_07': np.float64,
                    'tag_alert': np.str_, 'separation_alert': np.float64, 'name_alert': np.str_,
                    'x_alert': np.float64, 'y_alert': np.float64,
                    'tag_extra_alert': np.str_, 'separation_extra_alert': np.float64,
                    'name_extra_alert': np.str_,
                    'x_extra_alert': np.float64, 'y_extra_alert': np.float64,
                    'tag_extra_alert2': np.str_, 'separation_extra_alert2': np.float64,
                    'name_extra_alert2': np.str_,
                    'x_extra_alert2': np.float64, 'y_extra_alert2': np.float64,
                    'tag_extra_alert3': np.str_, 'separation_extra_alert3': np.float64,
                    'name_extra_alert3': np.str_,
                    'x_extra_alert3': np.float64, 'y_extra_alert3': np.float64
                    }
    sumi_df = pd.read_table(filepath_, delim_whitespace=True, header=None,
                                names=column_names,
                                comment='#', dtype=column_types)
    sumi_df['lightcurve_name'] = sumi_df['field'].astype(str) + '-' + sumi_df['band'].astype(
        str) + '-' + sumi_df['chip'].astype(str) \
                                     + '-' + sumi_df['subframe'].astype(str) + '-' + sumi_df['ID'].astype(
        str)
    return sumi_df


def alert_id_reader(
        filepath=f"/Users/sishitan/Documents/Scripts/qusi_project/qusi/data/moa_microlensing_550k/candlist_AlertID.dat.txt"):
    """
    Read the candlist_AlertID.dat file from nexsci website
    :param filepath:
    :return:
    """
    # x (pixel)
    # y (pixel)
    # RA  (2000)
    # Dec (2000)
    # separation to Alert position  (pixel)
    # Alert x (pixel)
    # Alert y (pixel)
    column_names_alertid = ['field', 'chip', 'subframe', 'ID',
                            'sumi_tag',
                            'x', 'y',
                            'RA', 'Dec',
                            'separation_alert', 'ID_alert', 'x_alert', 'y_alert',
                            'separation_extra_alert', 'ID_extra_alert', 'x_extra_alert', 'y_extra_alert']
    column_types_alertid = {'field': np.str_, 'chip': np.int_, 'subframe': np.int_, 'ID': np.int_,
                            'sumi_tag': np.str_,
                            'x': np.float64, 'y': np.float64,
                            'RA': np.str_, 'Dec': np.str_,
                            'separation_alert': np.float64, 'ID_alert': np.str_, 'x_alert': np.float64,
                            'y_alert': np.float64,
                            'separation_extra_alert': np.float64, 'ID_extra_alert': np.str_,
                            'x_extra_alert': np.float64, 'y_extra_alert': np.float64}
    alertid_df = pd.read_table(filepath, delim_whitespace=True, header=None,
                               names=column_names_alertid,
                               skiprows=13, dtype=column_types_alertid)
    alertid_df['lightcurve_name'] = alertid_df['field'].astype(str) + '-' + 'R' + '-' + alertid_df['chip'].astype(str) \
                                    + '-' + alertid_df['subframe'].astype(str) + '-' + alertid_df['ID'].astype(str)
    print()
    return alertid_df


def radec_reader(
        filepath=f"/Users/sishitan/Documents/Scripts/qusi_project/qusi/data/moa_microlensing_550k/candlist_RADec.dat.txt"):
    """
        Read the candlist_RADec.dat file from nexsci website
    :param filepath:
    :return:
    """
    # $field,               : field
    # $chip,                : chip
    # $nsub,                : subframe
    # $ID,                  : ID
    # $RA,                  : RA  (2000)
    # $Dec,                 : Dec (2000)
    # $x,                   : x in pixel
    # $y,                   : y in pixel
    # $ndata,               : number of datapoints
    # $ndetect,             : number of frames in which the object is detected
    # $sigma,               : significance at max significant point in light curve
    # $sumsigma,            : sum of significance of continuous significant points in light curve
    # $redchi2_out,         : chi square outside of the search window in light curve
    # $sepmin,              : separation in pix to the closest dohpot object in the reference image
    # $ID_dophot,           : dophot ID
    # $type,                : dophot type
    # $mag,                 : dophot mag
    # $mage,                : dophot mag error
    # $t0,                  : t0    (PSPL fit)
    # $tE,                  : tE    (PSPL fit)
    # $umin,                : u0    (PSPL fit)
    # $fs,                  : source flux    (PSPL fit)
    # $fb,                  : blending flux    (PSPL fit)
    # $t0e,                 : parabolic error in t0    (PSPL fit)
    # $tEe,                 : parabolic error in t_E    (PSPL fit)
    # $tEe1,                : lower limit error in t_E    (PSPL fit)
    # $tEe2,                : upper limit error in t_E    (PSPL fit)
    # $umine,               : parabolic error in u0    (PSPL fit)
    # $umine1,              : lower limit error in u0    (PSPL fit)
    # $umine2,              : upper limit error in u0    (PSPL fit)
    # $fse,                 : error in fs    (PSPL fit)
    # $fbe,                 : error in fb    (PSPL fit)
    # $chi2,                : chi^2    (PSPL fit)
    # $t0FS,                : t0    (FSPL fit)
    # $tEFS,                : tE    (FSPL fit)
    # $uminFS,              : u0    (FSPL fit)
    # $rhoFS,               : rho   (FSPL fit)
    # $fsFS,                : source flux    (FSPL fit)
    # $fbFS,                : blending flux    (FSPL fit)
    # $t0eFS,               : parabolic error in t0    (FSPL fit)
    # $tEeFS,               : parabolic error in t_E    (FSPL fit)
    # $tEe1FS,              : lower limit error in t_E    (FSPL fit)
    # $tEe2FS,              : upper limit error in t_E    (FSPL fit)
    # $umineFS,             : parabolic error in u0    (FSPL fit)
    # $umine1FS,            : lower limit error in u0    (FSPL fit)
    # $umine2FS,            : upper limit error in u0    (FSPL fit)
    # $rhoeFS,              : parabolic error in rho    (FSPL fit)
    # $rhoe1FS,             : lower limit error in rho    (FSPL fit)
    # $rhoe2FS              : upper limit error in rho    (FSPL fit)
    # $fseFS,               : error in fs    (FSPL fit)
    # $fbeFS,               : error in fb    (FSPL fit)
    # $chi2FS,              : chi^2    (FSPL fit)
    print(f'Reading {filepath} ...')
    column_names_radec = ['field', 'chip', 'subframe', 'ID', 'RA', 'Dec',
                          'x', 'y', 'ndata', 'ndetect', 'sigma', 'sumsigma', 'redchi2_out', 'sepmin',
                          'ID_dophot', 'type_', 'mag', 'mage', 't0', 'tE', 'umin', 'fs', 'fb', 't0e', 'tEe',
                          'tEe1', 'tEe2', 'umine', 'umine1', 'umine2', 'fse', 'fbe', 'chi2', 't0FS', 'tEFS',
                          'uminFS', 'rhoFS', 'fsFS', 'fbFS', 't0eFS', 'tEeFS', 'tEe1FS', 'tEe2FS', 'umineFS',
                          'umine1FS', 'umine2FS', 'rhoeFS', 'rhoe1FS', 'rhoe2FS', 'fseFS', 'fbeFS', 'chi2FS']
    column_types_radec = {'field': np.str_, 'chip': np.int_, 'subframe': np.int_, 'ID': np.int_,
                          'RA': np.str_, 'Dec': np.str_,
                          'x': np.float64, 'y': np.float64,
                          'ndata': np.int_, 'ndetect': np.int_,
                          'sigma': np.float64, 'sumsigma': np.float64, 'redchi2_out': np.float64,
                          'sepmin': np.float64, 'ID_dophot': np.float64, 'type_': np.float64,
                          'mag': np.float64, 'mage': np.float64, 't0': np.float64, 'tE': np.float64,
                          'umin': np.float64, 'fs': np.float64, 'fb': np.float64,
                          't0e': np.float64, 'tEe': np.float64,
                          'tEe1': np.float64, 'tEe2': np.float64, 'umine': np.float64,
                          'umine1': np.float64, 'umine2': np.float64, 'fse': np.float64, 'fbe': np.float64,
                          'chi2': np.float64, 't0FS': np.float64, 'tEFS': np.float64,
                          'uminFS': np.float64, 'rhoFS': np.float64, 'fsFS': np.float64, 'fbFS': np.float64,
                          't0eFS': np.float64, 'tEeFS': np.float64, 'tEe1FS': np.float64, 'tEe2FS': np.float64,
                          'umineFS': np.float64, 'umine1FS': np.float64, 'umine2FS': np.float64,
                          'rhoeFS': np.float64, 'rhoe1FS': np.float64, 'rhoe2FS': np.float64,
                          'fseFS': np.float64, 'fbeFS': np.float64, 'chi2FS': np.float64}
    radec_df = pd.read_table(filepath, delim_whitespace=True, header=None,
                             names=column_names_radec,
                             skiprows=53, dtype=column_types_radec)
    radec_df['lightcurve_name'] = radec_df['field'].astype(str) + '-' + 'R' + '-' + radec_df['chip'].astype(str) \
                                  + '-' + radec_df['subframe'].astype(str) + '-' + radec_df['ID'].astype(str)
    return radec_df


