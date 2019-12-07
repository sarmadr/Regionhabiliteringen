# import z3
from docplex.cp.model import CpoModel
import util
import json

# -----------------------------------------------------------------------------
# Parameters
# -----------------------------------------------------------------------------
# morning_start = 800  # military hours
# afternoon_end = 1600
segment_len = 15  # the smallest resolution of time segment in miutes


# -----------------------------------------------------------------------------
# Read problem data
# -----------------------------------------------------------------------------

# Read patient info:
patient_list = []

with open('patient_data.json', 'r') as f:
    patient_dict = json.load(f)

    for pat in patient_dict:
        temp_patient = util.PatientData()

        # General data
        temp_patient.id = len(patient_list)
        temp_patient.priority = pat['priority']
        temp_patient.name = pat['name']
        temp_patient.age = pat['age']
        temp_patient.nb_treatment_days = pat['treatment_days']

        # Treatment plan/resource usage
        # temp_patient.resource_usage = pat['activities']
        temp_patient.treatment_activities = util.group_treatment_activities(
            pat)
        patient_list.append(temp_patient)


# read doctor info
doctor_list = []  # Resources

with open('personnel_data.json', 'r') as f:
    doctor_dict = json.load(f)

    # Note the personnel_data.json is an array of similar types (dictionary).
    for doc in doctor_dict:
        temp_doc = util.DoctorData()
        temp_doc.skill = doc['profession']
        temp_doc.name = doc['name']
        temp_doc.working_time_limit = doc['working_time_limit']
        temp_doc.visit_time_pref = doc['visit_time_pref']
        temp_doc.id = len(doctor_list)  # NB! must be unique. Here set as idx.

        for time_segment in doc['unavailable_times']:
            temp_off = util.TimeSegment()
            temp_off.from_day = time_segment['from_day']
            temp_off.from_hour = time_segment['from_hour']
            temp_off.to_day = time_segment['to_day']
            temp_off.to_hour = time_segment['to_hour']
            temp_doc.unavailable_times.append(temp_off)

        doctor_list.append(temp_doc)


policy_data = util.PolicyData()
with open('policy_config.json', 'r') as f:
    policy_dict = json.load(f)
    # Policies are simple so use built-in dictionary
    policy_data.work_hours = policy_dict['work_hours']
    policy_data.lunch_break = policy_dict['lunch_break']
    policy_data.short_break = policy_dict['short_break']
    policy_data.other_activity_duration = policy_dict['other_activity_duration']
    policy_data.calendar_work_days = policy_dict['calendar_work_days']

# -----------------------------------------------------------------------------
# Create constants
# -----------------------------------------------------------------------------
# modeling the time.

# days_in_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']

hours_in_day = ['0800', '0815', '0830', '0845',
                '0900', '0915', '0930', '0945',
                '1000', '1015', '1030', '1045',
                '1100', '1115', '1130', '1145',
                '1200', '1215', '1230', '1245',
                '1300', '1315', '1330', '1345',
                '1400', '1415', '1430', '1445',
                '1500', '1515', '1530', '1545',
                '1600']

# Generate domain for a time variables.
time_seg_idx = []  # it's the scheduling horizon, maybe call it that.

for i in policy_data.calendar_work_days:
    for j in hours_in_day:
        time = util.Time(i, j, len(time_seg_idx))
        time_seg_idx.append(time)


# -----------------------------------------------------------------------------
# Optimization variables
# -----------------------------------------------------------------------------
# the main loop of making the variables.

mdl = CpoModel()
all_visits = []

# Set admittance variables.
for pat in patient_list:
    name = 'z_' + str(pat.id)
    pat.is_admitted_var = mdl.binary_var(name=name)

# follow indexing system of X_{k,i,j}^{l}: {doc,patient, visit session}, {day}
for doc in doctor_list:
    for pat in patient_list:

        if(doc.skill in pat.treatment_activities):  # then visit!

            days = policy_data.calendar_work_days[0:pat.nb_treatment_days]
            # For each mandatory session generate one S_kij variable,
            # and list of binary vars for each possible day
            for ses_idx, ses_dur in enumerate(pat.treatment_activities[doc.skill]):
                vis_idx = len(all_visits)
                vis = util.Visits(vis_idx, doc.name, doc.id, pat.name, pat.id)
                vis.set_session(ses_idx, ses_dur)

                # add s variable
                # NB! MAYBE LATER SET THE DOMAIN TO TAKE ALL POSSIBLE VALUES
                # OF THE WHOLE WCHEDULING HOROZON: to see if more patients
                # can be fit into the schedule.
                name = 'S_' + str(doc.id) + '_' + \
                    str(pat.id) + '_' + str(ses_idx)
                begin_seg_idx, end_seg_idx = util.get_start_end_time_idx(
                    days[0], days[-1],  time_seg_idx)

                vis.s_var = mdl.integer_var(
                    name=name, min=begin_seg_idx, max=end_seg_idx)

                # add binary variables for morning and afternoon possibility
                for day in days:
                    name = 'x_' + str(doc.id) + '_' + str(pat.id) + \
                        '_' + str(ses_idx) + '_' + str(day)
                    vis.x_vars.append(mdl.binary_var(name=name))

                    name = 'y_' + str(doc.id) + '_' + str(pat.id) + \
                        '_' + str(ses_idx) + '_' + str(day)

                    vis.y_vars.append(mdl.binary_var(name=name))

                # add day binary vars in a next for loop nested into this one

                # Store the visit in the global array, doctor, and patient arrays.
                all_visits.append(vis)
                doc.visit_vars.append(vis)
                if(doc.skill not in pat.visit_vars_dict):
                    pat.visit_vars_dict[doc.skill] = []
                pat.visit_vars_dict[doc.skill].append(vis)


# -----------------------------------------------------------------------------
# Constraints
# -----------------------------------------------------------------------------


'''
CONSTRAINT:
For the same# doctor and the same patient; One visit per day at most, a
doctor doesn't see the same patient more than# once, per day.

sum over j (x_{k,i,j}^{l} + y_{k,i,j}^{l} <= 1) ; \forall (k, i, l)
'''
for pat in patient_list:  # i
    for doc in pat.visit_vars_dict:  # k

        nb_doc_sessions = len(pat.visit_vars_dict[doc])  # j
        for l in range(pat.nb_treatment_days):
            cons = mdl.sum(pat.visit_vars_dict[doc][j].x_vars[l] +
                           pat.visit_vars_dict[doc][j].y_vars[l]
                           for j in range(nb_doc_sessions)) <= 1
            # print(cons)
            mdl.add(cons)


'''
CONSTRAINT:
Combination of two constraints in form of reified constraints:

(1) exactly one visit instance among all possible visit instances of the same
visit must be done, among all days of the scheduling horizon.

sum over l (x_{k,i,j}^{l} + y_{k,i,j}^{l} <= 1) ; \forall (k, i, j)

(2) If a patient is admitted, all his/her visit sessions must be done.
Hence, only if z_i == 1 the constraint above must hold
It's possible to manually force an admittance to happen, if it has waited
long enough, just by setting z_i=1 for patient i.
'''
for pat in patient_list:  # i
    for doc in pat.visit_vars_dict:  # k
        nb_doc_sessions = len(pat.visit_vars_dict[doc])  # j
        for j in range(nb_doc_sessions):
            cons = mdl.if_then(pat.is_admitted_var == 1,
                               mdl.sum(pat.visit_vars_dict[doc][j].x_vars[l] +
                                       pat.visit_vars_dict[doc][j].y_vars[l]
                                       for l in range(pat.nb_treatment_days)) == 1)
            # print(cons)
            mdl.add(cons)


'''
CONSTRAINT:
For the same patient and doctor, at least some visit sessions must happen
in the morning. This is because children become tired in the afternoon, and 
harder to work with, which makes it more difficult for the doctor to conduct
diagnosis. Hence each doctor wants to do at least some visits of the same
patient in the morning.

sum_sum_j_l( y_{k,i,j}^{l}) <= sum_sum_j_l(x_{k,i,j}^{l}) + 1 ; \forall (k, i)
'''
for pat in patient_list:  # i
    for doc in pat.visit_vars_dict:  # k
        nb_doc_sessions = len(pat.visit_vars_dict[doc])  # j
        cons = (mdl.sum(pat.visit_vars_dict[doc][j].y_vars[l]
                        for j in range(nb_doc_sessions)
                        for l in range(pat.nb_treatment_days)) <=

                mdl.sum(pat.visit_vars_dict[doc][j].x_vars[l]
                        for j in range(nb_doc_sessions)
                        for l in range(pat.nb_treatment_days)) + 1)
        # print(cons)
        mdl.add(cons)


'''
CONSTRAINT:
Connect high-level binary day variables with low-level integer time variables.

(1): if a visit is done in the morning, limit the time_variables to be in
the morning; alpha is the index of day l @ '0800', and betta is index of the
same day l @ '1200'. The exact hours enforced to the constraint may be changed
based on need of the team. For example, maybe visit must end before '1100', in
which case, betta is set to '1100'

if(x_{k,i,j}^{l} == 1) ==> alpha<= s_{k,i,j} + D_{k,i,j} <= betta;
\forall (k, i, j, l)

(2): Same as (1), but for the afternoon variables y_{k,i,j}^{l}
'''
for pat in patient_list:  # i
    for doc in pat.visit_vars_dict:  # k
        nb_doc_sessions = len(pat.visit_vars_dict[doc])  # j
        for j in range(nb_doc_sessions):

            # some sessions have longer lengts; ex. arebetstera. has 45/120
            dur = int(pat.visit_vars_dict[doc][j]._session_dur / segment_len)

            days = policy_data.calendar_work_days[0:pat.nb_treatment_days]

            for l_idx, l_val in enumerate(days):
                vis_s = util.get_time_idx(l_val, '0800', time_seg_idx)
                vis_e = util.get_time_idx(l_val, '1200', time_seg_idx)

                # morning
                cons_ub_am = mdl.if_then(pat.visit_vars_dict[doc][j].x_vars[l_idx] == 1,
                                         pat.visit_vars_dict[doc][j].s_var + dur <= vis_e)

                cons_lb_am = mdl.if_then(pat.visit_vars_dict[doc][j].x_vars[l_idx] == 1,
                                         vis_s <= pat.visit_vars_dict[doc][j].s_var)

                # afternoon
                cons_ub_pm = mdl.if_then(pat.visit_vars_dict[doc][j].y_vars[l_idx] == 1,
                                         pat.visit_vars_dict[doc][j].s_var + dur <= vis_e)

                cons_lb_pm = mdl.if_then(pat.visit_vars_dict[doc][j].y_vars[l_idx] == 1,
                                         vis_s <= pat.visit_vars_dict[doc][j].s_var)

                mdl.add(cons_ub_am)
                mdl.add(cons_lb_am)
                mdl.add(cons_ub_pm)
                mdl.add(cons_lb_pm)



'''
Objective function:
maximize the number of admitted patients.
'''
nb_admitted_patients = mdl.integer_var()
mdl.add(nb_admitted_patients == mdl.sum(
    pat.is_admitted_var for pat in patient_list))
mdl.add(mdl.maximize(nb_admitted_patients))

# Solve
msol = mdl.solve(LogVerbosity='Quiet', Workers=1)
print("Solution status: " + msol.get_solve_status())
if msol:
    print('nb_admitted_patients = ', msol.get_objective_values()[0])


#print(util.get_time_idx(12, '0800', time_seg_idx))

print('Done!')
