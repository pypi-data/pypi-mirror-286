from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, Field
from pydantic_extra_types.color import Color
from pydantic_extra_types.coordinate import Coordinate, Latitude, Longitude

from lijnpy import _logger
from lijnpy._rest_adapter import DeLijnAPIException
from lijnpy.enums import (
    Accessibility,
    Language,
    LineDirection,
    OperationType,
    TransportType,
)


class GeoCoordinate(Coordinate):
    """A geographical coordinate with a latitude and longitude

    Attributes:
        latitude (Latitude): The latitude of the coordinate
        longitude (Longitude): The longitude of the coordinate
    """

    latitude: Latitude
    longitude: Longitude


class DetourPeriod(BaseModel):
    """A period of a detour of a line

    Attributes:
        start_date (datetime): The start date of the period
        end_date (datetime, optional): The end date of the period. Defaults to None.
    """

    start_date: datetime = Field(validation_alias="startDatum")
    end_date: datetime | None = Field(default=None, validation_alias="eindDatum")


class Stop(BaseModel):
    """A bus stop

    Attributes:
        entity_number (int): The number of the entity
        number (int): The number of the stop
        description (str, optional): The description of the stop. Defaults to None.
        description_long (str): The long description of the stop
        municipality_number (int): The number of the municipality
        municipality_description (str): The description of the municipality
        geo_coordinate (GeoCoordinate): The geographical coordinate of the stop
        accessibilities (list[Accessibility]): The accessibilities of the stop
        is_main (bool, optional): Whether the stop is the main stop. Defaults to None.
        language (Language): The language of the stop
    """

    entity_number: int = Field(validation_alias="entiteitnummer")
    number: int = Field(validation_alias="haltenummer")
    description: str | None = Field(default=None, validation_alias="omschrijving")
    description_long: str = Field(validation_alias="omschrijvingLang")
    municipality_number: int = Field(validation_alias="gemeentenummer")
    municipality_description: str = Field(validation_alias="omschrijvingGemeente")
    geo_coordinate: GeoCoordinate = Field(validation_alias="geoCoordinaat")
    accessibilities: list[Accessibility] = Field(
        validation_alias="halteToegankelijkheden"
    )
    is_main: bool | None = Field(default=None, validation_alias="hoofdHalte")
    language: Language = Field(validation_alias="taal")


class Line(BaseModel):
    """A bus line

    Attributes:
        entity_number (int): The number of the entity
        line_number (int): The number of the line
        line_number_public (str): The public number of the line
        description (str): The description of the line
        transport_region_code (str): The code of the transport region
        is_public (bool): Whether the line is public
        transport_type (str): The type of the transport
        operation_type (str): The type of the operation
        valid_from (str): The valid from date of the line
        valid_to (str, optional): The valid to date of the line. Defaults to None.
    """

    entity_number: int = Field(validation_alias="entiteitnummer")
    line_number: int = Field(validation_alias="lijnnummer")
    line_number_public: str = Field(validation_alias="lijnnummerPubliek")
    description: str = Field(validation_alias="omschrijving")
    transport_region_code: str = Field(validation_alias="vervoerRegioCode")
    is_public: bool = Field(validation_alias="publiek")
    transport_type: TransportType = Field(validation_alias="vervoertype")
    operation_type: OperationType = Field(validation_alias="bedieningtype")
    valid_from: date = Field(validation_alias="lijnGeldigVan")
    valid_to: date = Field(validation_alias="lijnGeldigTot")


class Entity(BaseModel):
    """An entity

    Attributes:
        number (int): The number of the entity
        code (str): The code of the entity
        description (str): The description of the entity
    """

    number: int = Field(validation_alias="entiteitnummer")
    code: str = Field(validation_alias="entiteitcode")
    description: str = Field(validation_alias="omschrijving")


class LineColor(BaseModel):
    """A color of a bus line

    Attributes:
        code (str): The code of the color
        description (str): The description of the color
        color (Color): The color of the line
    """

    code: str
    description: str = Field(validation_alias="omschrijving")
    color: Color = Field(validation_alias="hex")


class Municipality(BaseModel):
    """A municipality in Belgium

    Attributes:
        number (int): The number of the municipality
        description (str): The description of the municipality
        main_municipality (Municipality | None, optional): The main municipality of the municipality. Defaults to None.
    """

    number: int = Field(validation_alias="gemeentenummer")
    description: str = Field(validation_alias="omschrijving")
    main_municipality: Municipality | None = Field(
        default=None, validation_alias="hoofdGemeente"
    )


class StopInVicinity(BaseModel):
    """A stop in the vicinity of a geographical coordinate

    Attributes:
        type (str): The type of the stop
        id (int): The id of the stop
        name (str): The name of the stop
        distance (int): The distance of the stop
        geo_coordinate (GeoCoordinate): The geographical coordinate of the stop
    """

    # TODO: enum for type
    type: str
    id: int
    name: str = Field(validation_alias="naam")
    distance: int = Field(validation_alias="afstand")
    geo_coordinate: GeoCoordinate = Field(validation_alias="geoCoordinaat")


class Passage(BaseModel):
    """A passage of a bus line

    Attributes:
        entity_number (int): The number of the entity
        line_number (int): The number of the line
        direction (str): The direction of the line
        ride_number (int): The number of the ride
        destination (str): The destination of the ride
        destination_place (str): The place of the destination
        vias (list[str], optional): The vias of the ride. Defaults to None.
        timetable_timestamp (datetime): The timestamp of the timetable
    """

    entity_number: int = Field(validation_alias="entiteitnummer")
    line_number: int = Field(validation_alias="lijnnummer")
    direction: LineDirection = Field(validation_alias="richting")
    ride_number: int = Field(validation_alias="ritnummer")
    destination: str = Field(validation_alias="bestemming")
    destination_place: str = Field(validation_alias="plaatsBestemming")
    vias: list[str] | None = None
    timetable_timestamp: datetime = Field(validation_alias="dienstregelingTijdstip")


class TransportRegion(BaseModel):
    """A transport region in Belgium

    Attributes:
        code (str): The code of the transport region
        name (str): The name of the transport region
        number (str): The number of the transport region
    """

    code: str
    name: str = Field(validation_alias="naam")
    number: int = Field(validation_alias="nr")


class RideNote(BaseModel):
    """A note for a ride

    Attributes:
        id (int): The id of the note
        title (str): The title of the note
        ride_number (int): The number of the ride
        stop_number (int): The number of the stop
        description (str): The description of the note
        entity_number (int): The number of the entity
        line_number (int): The number of the line
        direction (LineDirection): The direction of the line
    """

    id: int
    title: str = Field(validation_alias="titel")
    ride_number: int = Field(validation_alias="ritnummer")
    stop_number: int = Field(validation_alias="haltenummer")
    description: str = Field(validation_alias="omschrijving")
    entity_number: int = Field(validation_alias="entiteitnummer")
    line_number: int = Field(validation_alias="lijnnummer")
    direction: LineDirection = Field(validation_alias="richting")


class PassageNote(BaseModel):
    """A note for a passage

    Attributes:
        id (int): The id of the note
        title (str): The title of the note
        ride_number (int): The number of the ride
        stop_number (int): The number of the stop
        description (str): The description of the note
        entity_number (int): The number of the entity
        line_number (int): The number of the line
        direction (LineDirection): The direction of the line
    """

    id: int
    title: str = Field(validation_alias="titel")
    ride_number: int = Field(validation_alias="ritnummer")
    stop_number: int = Field(validation_alias="haltenummer")
    description: str = Field(validation_alias="omschrijving")
    entity_number: int = Field(validation_alias="entiteitnummer")
    line_number: int = Field(validation_alias="lijnnummer")
    direction: LineDirection = Field(validation_alias="richting")


class Timetable(BaseModel):
    """A timetable of a stop

    Attributes:
        passages (list[Passage]): The passages of the schedule
        passage_notes (list[PassageNote]): The notes of the passages
        ride_notes (list[RideNote]): The notes of the rides
        detours (list[Detour]): The detours of the schedule
    """

    passages: list[Passage]
    passage_notes: list[PassageNote] = Field(validation_alias="doorkomstNotas")
    ride_notes: list[RideNote] = Field(validation_alias="ritNotas")
    detours: list[Detour] = Field(validation_alias="omleidingen")

    def __init__(self, **kwargs):
        try:
            kwargs["passages"] = kwargs["halteDoorkomsten"][0]["doorkomsten"]
        except KeyError as e:
            _logger.error(f"Failed to parse the response from the API: {e}")
            raise DeLijnAPIException from e
        super().__init__(**kwargs)


class Direction(BaseModel):
    """A direction of a line

    Attributes:
        entity_number (int): The number of the entity
        line_number (int): The number of the line
        direction (LineDirection): The direction of the line
        description (str): The description of the direction
    """

    entity_number: int = Field(validation_alias="entiteitnummer")
    line_number: int = Field(validation_alias="lijnnummer")
    direction: LineDirection = Field(validation_alias="richting")
    description: str = Field(validation_alias="omschrijving")


class Detour(BaseModel):
    """A detour of a line

    Attributes:
        title (str): The title of the detour
        description (str): The description of the detour
        period (DetourPeriod): The period of the detour
        directions (list[Direction]): The directions of the detour
        detour_reference (int): The reference of the detour
        detour_days (list[str]): The days of the detour
    """

    title: str = Field(validation_alias="titel")
    description: str = Field(validation_alias="omschrijving")
    period: DetourPeriod = Field(validation_alias="periode")
    directions: list[Direction] = Field(validation_alias="lijnrichtingen")
    detour_reference: int = Field(validation_alias="referentieOmleiding")
    detour_days: list[str] = Field(validation_alias="omleidingsDagen")


class RealTimePassage(BaseModel):
    """A real-time passage of a bus line

    Attributes:
        entity_number (int): The number of the entity
        line_number (int): The number of the line
        direction (LineDirection): The direction of the line
        ride_number (int): The number of the ride
        destination (str): The destination of the ride
        vias (list[str], optional): The vias of the ride. Defaults to None.
        timetable_timestamp (datetime): The timestamp of the timetable
        real_time_timestamp (datetime): The timestamp of the real-time
        vrtnum (int): The number of the real-time
        prediction_statuses (list[str]): The statuses of the prediction
    """

    entity_number: int = Field(validation_alias="entiteitnummer")
    line_number: int = Field(validation_alias="lijnnummer")
    direction: LineDirection = Field(validation_alias="richting")
    ride_number: int = Field(validation_alias="ritnummer")
    destination: str = Field(validation_alias="bestemming")
    vias: list[str] | None = Field(default=None)
    timetable_timestamp: datetime = Field(validation_alias="dienstregelingTijdstip")
    real_time_timestamp: datetime = Field(validation_alias="real-timeTijdstip")
    vrtnum: int
    prediction_statuses: list[str] = Field(validation_alias="predictionStatussen")


class RealTimeStopPassage(BaseModel):
    """All real-time passages of a bus stop

    Attributes:
        passages (list[RealTimePassage]): The real-time passages of a bus stop
    """

    passages: list[RealTimePassage] = Field(validation_alias="doorkomsten")


class RealTimeTimetable(BaseModel):
    """A real-time timetable of a stop

    Attributes:
        passages (list[RealTimePassage]): The real-time arrivals of the stop
        passage_notes (list[PassageNote]): The notes of the passages
        ride_notes (list[RideNote]): The notes of the rides
        detours (list[Detour]): The detours of the stop
    """

    passages: list[RealTimePassage]
    passage_notes: list[PassageNote] = Field(validation_alias="doorkomstNotas")
    ride_notes: list[RideNote] = Field(validation_alias="ritNotas")
    detours: list[Detour] = Field(validation_alias="omleidingen")

    def __init__(self, **kwargs):
        try:
            kwargs["passages"] = kwargs["halteDoorkomsten"][0]["doorkomsten"]
        except KeyError as e:
            _logger.error(f"Failed to parse the response from the API: {e}")
            raise DeLijnAPIException from e
        super().__init__(**kwargs)


class Disruption(BaseModel):
    """A disruption of a line

    Attributes:
        description (str): The description of the disruption
        line_directions (list[Direction]): The directions of the line
    """

    description: str = Field(validation_alias="omschrijving")
    line_directions: list[Direction] = Field(validation_alias="lijnrichtingen")
