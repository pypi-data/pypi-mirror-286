def CustomDataStruct():
    from .Data.dataquery import DataStruct as BaseDataStruct

    CustomDataStruct = BaseDataStruct(
        survey=None,
        catalogue=None,
        source=None,
        pos=None,
        identifier=None,
        data=None,
    )

    CustomDataStruct.subkind = None

    return CustomDataStruct


def CustomLightcurveStruct():
    from .Data.lightcurvequery import LightcurveStruct as BaseLightcurveStruct

    CustomLightcurveStruct = BaseLightcurveStruct(
        survey=None, source=None, pos=None, identifier=None, data=None
    )

    return CustomLightcurveStruct


def CustomImageStruct():
    from .Data.imagequery import ImageStruct as BaseImageStruct

    CustomImageStruct = BaseImageStruct(survey=None, source=None, pos=None, data=None)

    return CustomImageStruct


def CustomHrdStruct():
    from .Data.hrdquery import HrdStruct as BaseHrdStruct

    CustomHrdStruct = BaseHrdStruct(sources=None, data=None)

    return CustomHrdStruct


def CustomSedStruct():
    from .Data.sedquery import SedStruct as BaseSedStruct

    CustomSedStruct = BaseSedStruct(source=None, pos=None, data=None)

    return CustomSedStruct


def CustomSpectrumStruct():
    from .Data.spectrumquery import SpectrumStruct as BaseSpectrumStruct

    CustomSpectrumStruct = BaseSpectrumStruct(
        survey=None, source=None, pos=None, data=None
    )

    return CustomSpectrumStruct
