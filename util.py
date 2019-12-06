'''
Keeps the utility classes and functions.
'''

class TimeSegment:
    '''
    Defnition of a time segment.

    * Example:
    from_day = 'Mon', from_time = '0900'
    to_day = 'Mon', to_time = '1300'
    '''

    def __init__(self):

        # self.time_stamp = None
        self.from_day = None
        self.from_hour = None

        self.to_day = None
        self.to_hour = None


class PatientData:
    '''
    Holds information about a patient.

    Attributes:
    id -- unique patient identifier.
    visit_vars -- dict{'doctor_type': list<Visits()>} 
    is_admitted_var -- boolian decision variable. The value is decided by the
    sovler.
    '''

    def __init__(self):
        self.priority = None  # based on their queue time
        self.name = None
        self.age = None  # above a certain threshold considered "older kid".
        self.nb_treatment_days = None  # above 5 days will be two-week period.
        self.treatment_activities = {}
        self.id = None

        self.visit_vars_dict = {}
        self.is_admitted_var = None


def group_treatment_activities(patient_dic):
    '''
    Loop over stream of treatment plan of patient a and return
    dict<dict<list>> of resource usages grouped together.

    Based on the treatment activities of a patient identify what resources
    (skills) are needed, and for how long. Take care of cases when usages of
    the same resource are not all grouped together.

    Keyword arguments
    activities --  a dictionary of patient info with the key "activities"
    '''
    grouped_resources = {}
    for activity in patient_dic['activities']:
        # the conversion to list is necessary: see
        # https://stackoverflow.com/questions/17322668/typeerror-dict-keys-object-does-not-support-indexing
        key = list(activity.keys())[0]
        val = activity[key]
        if key in grouped_resources:
            grouped_resources[key].append(val)
        else:
            grouped_resources[key] = [val]

    return grouped_resources


def identify_resource(doctor_list):
    '''
    Identify resources and their sizes and return them with their ids
    as dict<list>.

    Keyword arguments:
    doctor_list -- list<DoctorData> of doctors, possibly parsed from json.
    '''
    resource_dict = {}
    for doctor in doctor_list:
        if(doctor.skill not in resource_dict):
            resource_dict[doctor.skill] = [doctor.id]
        else:
            resource_dict[doctor.skill].append(doctor.id)

    return resource_dict


def identify_resource_usage(resource_ids, patient_list):
    '''
    Go through the treatment plan of patines and return activities,
    pertaining patient id, and activity durations.
    Return type is dict<list<pair>>. A pair is (patient_id, visit_duration).

    Keyword arguments:
    resource_ids -- dict<list>
    patient_list -- list<PatientData>
    '''
    resource_usages = {}

    for patient in patient_list:
        activities = list(patient.treatment_activities.keys())
        for skill in activities:
            # add the key
            if(skill not in resource_usages):
                resource_usages[skill] = []
            for duration in patient.treatment_activities[skill]:
                resource_usages[skill].append((patient.id, duration))

    return resource_usages


""" class PatientVar:
    '''
    Holds variables for a patient.

    * Example: logoped_start_list: hold optimization start_time variables for each
    visit of a logoped. This is equivalent of an 'operation' in an abstract
    sense.

    ** If a list is empty, the pertaining specialist will not have any visits
    for that child.
    '''

    def __init__(self):

        #  Visit start variables
        #self.lakare_start_vars = []
        #self.logoped_start_vars = []
        #self.fysioterap_start_vars = []
        #self.arbetsterap_start_vars = []
        #self.psykolog_start_vars = []
        #self.pedagog_start_vars = []

        # Visit end variables
        self.lakare_end_vars = []
        #self.logoped_start_vars = []
        #self.fysioterap_start_vars = []
        #self.arbetsterap_start_vars = []
        #self.psykolog_start_vars = []
        #self.pedagog_start_vars = []

        self.start_vars = []  # list of dictionary
        self.end_vars = [] """


class DoctorData:
    '''Hold information about a doctor.

    Attributes:
    unavailable_times -- populate with objects of TimeSegment.
    visit_preference -- 'AM' or 'PM'
    working_time_limit -- hours
    id -- unique if of doctor.
    visit_vars -- list of instances of Visits()
    '''

    def __init__(self):
        self.skill = None
        self.name = None
        self.working_time_limit = None  # hours
        self.visit_time_pref = None
        self.unavailable_times = []
        self.id = None

        self.visit_vars = []
    

    


class PolicyData:
    '''
    Holds parsed information from 'policy_config.json' file.
    The data members are dictionaries. Some dictionaries may have arrays
    as elements.
    '''

    def __init__(self):
        self.work_hours = None
        self.lunch_break = None
        self.short_break = None
        self.other_activity_duration = None
        self.calendar_work_days = []


class DoctorVisits:
    '''
    Hold arrays of patiensts with their arrays of variables of for.

    #Attributes:

    ** patients_list -- holds list of instances of PatientSameDoctorVars.
    **id -- current doctor's id.
    '''

    def __init__(self, doc_id, profession):
        self.patients_list = []
        self.id = doc_id
        self.skill = profession


class DoctorVisitsVars(DoctorVisits):
    '''
    Holds variables modeling visits of a doctor. Inherits from DoctorVisits.
    '''

    def __init__(self, doc_id, profession):
        DoctorVisits.__init__(self, doc_id, profession)


class PatientVisits():
    ''' Hold information on visits done on the same patient by the same doctor. '''

    def __init__(self, patient_id, patient_name):
        # dictionary: keys are days, value are lists of days.
        self.visits_dict = {}
        self.id = patient_id
        self.patient_name = patient_name

    def add_visit_day(self, day_str):
        '''Add an new day in patients visit calendar.'''

        assert(day_str not in self.visits_dict)
        self.visits_dict[day_str] = []

    def add_visit_option(self, day_str, duration):
        '''Add a single visit slot to a particular day.'''

        self.visits_dict[day_str].append(duration)

    # def add_variables


class PatientVisitsVars():

 
    def __init__(self, patient_id, patient_name):
        # dictionary: keys are days, value are lists of days.
        self.patient_id = patient_id
        self.patient_name = patient_name

        self.visits_morning_vars = {}  # x_{ij,k}^{l}
        self.visits_afternoon_vars = {}  # y_{ij,k}^{l}
        self.visits_hours_vars = []  # s_{ijk}





class Time():
    ''' '''

    def __init__(self, day, hours, idx):
        self._idx = idx
        self._day = day
        self._hours = hours


def get_start_end_time_idx(start_day, end_day, time_seg_idx):
    ''' '''
    begin_seg_idx = None
    end_seg_idx = None
    for seg in time_seg_idx:
        if(seg._day == start_day):
            begin_seg_idx = seg._idx
            break
    for seg in reversed(time_seg_idx):
        if(seg._day == end_day):
            end_seg_idx = seg._idx
            break

    return begin_seg_idx, end_seg_idx


class Visits():
    '''
    idx -- global index of the class in the list of all visits. 
    A VISIT is a possible realization of a manadotry SESSION. For example, if
    a doctor must visit a patient 3 times during 5 days, each of the mandatory
    sessions may happen in any of the days, hence different possibilities for
    a visit.

    Attributes:
    * x_vars -- list of binary variables modeling if a mandatory visit of
    session (k,i,j) is done in the morning of day l
    
    * y_vars -- list of binary variables modeling if a mandatory visit of
    session (k,i,j) is done in the afternoon of day l
    
    * s_var -- integer variable modeling the possible visit time of a
    mandatory session whose domain is index of time segments  defined
    over the entire rage of presence of the patient for treatment.

    '''

    def __init__(self, idx, doc_name, doc_id, patient_name, patient_id):
        '''Deafault Constructor'''

        self._patient_name = patient_name
        self._patient_id = patient_id
        self._doc_name = doc_name
        self._doc_id = doc_id
        self.visit_idx = idx

        self._session_idx = None
        self._session_dur = None
        
        #self.days = [] # maybe also add a list for possible time indices. 
        # so we have both calendar days, and indices that reflect exact hours
        # in the calendar.

        self.x_vars = []
        self.y_vars = []
        self.s_var = None

    def set_session(self, session_idx, session_dur):
        ''' Set the mandatory session.'''

        self._session_dur = session_dur
        self._session_idx = session_idx


