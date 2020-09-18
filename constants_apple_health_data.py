EXPORT_DATE = 'ExportDate'
ME = 'Me'
RECORD = 'Record'
CORRELATION = 'Correlation'
WORKOUT = 'Workout'
ACTIVITY_SUMMARY = 'ActivitySummary'
CLINICAL_RECORD = 'ClinicalRecord'


HEALTH_ROOT_CHILDREN = {
    EXPORT_DATE,
    ME,
    RECORD,
    CORRELATION,
    CLINICAL_RECORD,
    ACTIVITY_SUMMARY,
    WORKOUT
}

Fieldnames_ExportData = ['value']


HK_REC_TYPE_AppleStandHour = 'HKCategoryTypeIdentifierAppleStandHour'
HK_REC_TYPE_AudioExposureEvent = 'HKCategoryTypeIdentifierAudioExposureEvent'
HK_REC_TYPE_SleepAnalysis = 'HKCategoryTypeIdentifierSleepAnalysis'
HK_REC_TYPE_ActiveEnergyBurned = 'HKQuantityTypeIdentifierActiveEnergyBurned'
HK_REC_TYPE_AppleExerciseTime = 'HKQuantityTypeIdentifierAppleExerciseTime'
HK_REC_TYPE_AppleStandTime = 'HKQuantityTypeIdentifierAppleStandTime'
HK_REC_TYPE_BasalEnergyBurned = 'HKQuantityTypeIdentifierBasalEnergyBurned'
HK_REC_TYPE_BloodPressureDiastolic = 'HKQuantityTypeIdentifierBloodPressureDiastolic'
HK_REC_TYPE_BloodPressureSystolic = 'HKQuantityTypeIdentifierBloodPressureSystolic'
HK_REC_TYPE_BodyFatPercentage = 'HKQuantityTypeIdentifierBodyFatPercentage'
HK_REC_TYPE_BodyMass = 'HKQuantityTypeIdentifierBodyMass'
HK_REC_TYPE_BodyMassIndex = 'HKQuantityTypeIdentifierBodyMassIndex'
HK_REC_TYPE_DietaryCholesterol = 'HKQuantityTypeIdentifierDietaryCholesterol'
HK_REC_TYPE_DistanceWalkingRunning = 'HKQuantityTypeIdentifierDistanceWalkingRunning'
HK_REC_TYPE_WalkingDoubleSupportPct = 'HKQuantityTypeIdentifierWalkingDoubleSupportPercentage'
HK_REC_TYPE_EnvironmentalAudioExposure = 'HKQuantityTypeIdentifierEnvironmentalAudioExposure'
HK_REC_TYPE_FlightsClimbed = 'HKQuantityTypeIdentifierFlightsClimbed'
HK_REC_TYPE_HeadphoneAudioExposure = 'HKQuantityTypeIdentifierHeadphoneAudioExposure'
HK_REC_TYPE_HeartRate = 'HKQuantityTypeIdentifierHeartRate'
HK_REC_TYPE_HeartRateVariabilitySDNN = 'HKQuantityTypeIdentifierHeartRateVariabilitySDNN'
HK_REC_TYPE_Height = 'HKQuantityTypeIdentifierHeight'
HK_REC_TYPE_LeanBodyMass = 'HKQuantityTypeIdentifierLeanBodyMass'
HK_REC_TYPE_RestingHeartRate = 'HKQuantityTypeIdentifierRestingHeartRate'
HK_REC_TYPE_StepCount = 'HKQuantityTypeIdentifierStepCount'
HK_REC_TYPE_VO2Max = 'HKQuantityTypeIdentifierVO2Max'
HK_REC_TYPE_WaistCircumference = 'HKQuantityTypeIdentifierWaistCircumference'
HK_REC_TYPE_WalkingHeartRateAverage = 'HKQuantityTypeIdentifierWalkingHeartRateAverage'
HK_REC_TYPE_WalkingSpeed ='HKQuantityTypeIdentifierWalkingSpeed'
HK_REC_TYPE_WalkingStepLength = 'HKQuantityTypeIdentifierWalkingStepLength'


FIELD_DATE = 'dateComponents'
FIELD_VALUE = 'value'
FIELD_UNIT = 'unit'
FIELD_TYPE = 'type'

FIELD_START_DATE = 'startDate'
FIELD_END_DATE = 'endDate'
FIELD_CREATION_DATE = 'creationDate'
FIELD_DEVICE = 'device'
FIELD_SOURCE_NAME = 'sourceName'
FIELD_SOURCE_VERSION = 'sourceVersion'

FIELD_WORKOUT_ACTIVITY = 'workoutActivityType'
FIELD_DURATION = 'duration'
FIELD_DURATION_UNIT = 'durationUnit'
FIELD_TOTAL_DISTANCE = 'totalDistance'
FIELD_TOTAL_DISTANCE_UNIT = 'totalDistanceUnit'
FIELD_TOTAL_ENERGY_BURNED = 'totalEnergyBurned'
FIELD_TOTAL_ENERGY_BURNED_UNIT = 'totalEnergyBurnedUnit'

Fieldnames_Record = [
    FIELD_TYPE,
    FIELD_UNIT,
    FIELD_VALUE,
    FIELD_SOURCE_NAME, 
    FIELD_SOURCE_VERSION,
    FIELD_DEVICE, 
    FIELD_CREATION_DATE, 
    FIELD_START_DATE,
    FIELD_END_DATE
]

Fieldnames_ActivitySummary = [
    FIELD_DATE,
    'activeEnergyBurned',
    'activeEnergyBurnedGoal',
    'activeEnergyBurnedUnit',
    'appleMoveTime',
    'appleMoveTimeGoal',
    'appleExerciseTime',
    'appleExerciseTimeGoal',
    'appleStandHours',
    'appleStandHoursGoal'
]

Fieldnames_ClinicalRecord = [
    FIELD_TYPE,
    'identifier',
    FIELD_SOURCE_NAME,
    'sourceURL',
    'fhirVersion',
    'receivedDate',
    'resourceFilePath',
]

Fieldnames_Correlation = [
    FIELD_TYPE,
    FIELD_SOURCE_NAME,
    FIELD_SOURCE_VERSION,
    FIELD_DEVICE,
    FIELD_CREATION_DATE,
    FIELD_START_DATE,
    FIELD_END_DATE
]


Fieldnames_Workout = [
    'workoutActivityType',
    FIELD_DURATION,
    FIELD_DURATION_UNIT,
    FIELD_TOTAL_DISTANCE,
    FIELD_TOTAL_DISTANCE_UNIT,
    FIELD_TOTAL_ENERGY_BURNED,
    FIELD_TOTAL_ENERGY_BURNED_UNIT,
    FIELD_SOURCE_NAME,
    FIELD_SOURCE_VERSION,
    FIELD_DEVICE,
    FIELD_CREATION_DATE,
    FIELD_START_DATE,
    FIELD_END_DATE
]


Fieldnames_Workout_MetadataEntry = [
    'HKIndoorWorkout',
    'HKAverageMETs',
    'HKWeatherTemperature',
    'HKWeatherHumidity',
    'HKTimeZone',
    'HKElevationAscended'
]

Fieldnames_Workout_Csv = Fieldnames_Workout + Fieldnames_Workout_MetadataEntry
workout_metadata_fields_set = set(Fieldnames_Workout_MetadataEntry)

WORKOUT_RUN = "HKWorkoutActivityTypeRunning"
WORKOUT_WALK = "HKWorkoutActivityTypeWalking"

csv_date = "date"
csv_body_mass = "bodymass"
csv_unit = "unit"
csv_movement_distance = "movement_distance"
csv_step_count = "step_count"
csv_vo2max = "vo2max"
csv_waist = "waist"
csv_duration = "duration"
csv_duration_unit = "duration_unit"
csv_distance = "distance"
csv_distance_unit = "distance_unit"
csv_energy_burned = "energy_burned"
csv_energy_burned_unit = "energy_burned_unit"

csv_fieldnames_bodymass_summary = [csv_date, csv_body_mass, csv_unit]
csv_fieldnames_distance_walking_running_summary = [csv_date, csv_movement_distance, csv_unit]
csv_fieldnames_step_count_summary = [csv_date, csv_step_count, csv_unit]
csv_fieldnames_vo2max_summary = [csv_date, csv_vo2max, csv_unit]
csv_fieldnames_workout_summary = [csv_date, csv_duration, csv_duration_unit, csv_distance,
                                  csv_distance_unit, csv_energy_burned, csv_energy_burned_unit]
csv_fieldnames_waist2piR_summary = [csv_date, csv_waist, csv_unit]

