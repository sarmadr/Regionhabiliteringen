'''
The utility classes and functions.
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


class Time():
    ''' '''

    def __init__(self, day, hours, idx):
        self._idx = idx
        self._day = day
        self._hours = hours


def get_start_end_time_idx(start_day, end_day, time_seg_idx):
    '''
    Return the start and end indices of a time period given the time horizon.

    Attributes:
    * start_day -- start day number as calendar day.
    * end_day -- end day number as calendar day.
    * time_seg_idx --- list of objects of Time(), as time segments.

    '''
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


def get_time_idx(day, time_str, time_seg_idx):
    '''
    Return the index of a time segment given its day number and military hours.

    Attributes:
    * day -- day number as calendar day.
    * time_str -- military time as string. Example: '0815' is 8:15.
    * time_seg_idx --- list of objects of Time(), as time segments.
    '''

    idx = None
    for seg in time_seg_idx:
        if(day == seg._day and time_str == seg._hours):
            idx = seg._idx

    if(idx is not None):
        return idx
    else:
        raise ValueError('Time segment not found!')


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

        # self.days = [] # maybe also add a list for possible time indices.
        # so we have both calendar days, and indices that reflect exact hours
        # in the calendar.

        self.x_vars = []
        self.y_vars = []
        self.s_var = None

    def set_session(self, session_idx, session_dur):
        ''' Set the mandatory session.'''

        self._session_dur = session_dur
        self._session_idx = session_idx


def no_overlap_ilog(s1, s2, d1, d2, mdl):
    '''

    '''
    return mdl.logical_or(s1 + d1 <= s2, s2 + d2 <= s1)
