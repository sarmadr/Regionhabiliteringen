Optimization code for doctor/patient scheduling

A sample schedule obtained from the optimizer looks as follows:

(calendar_day, time, doctor_to_visit, visit_duration)
---------------------------------------------------------------
The following is a solution obtained from an input file with 3 patients. One
patient needs one week (calendar days from 1 to 5), and the other two patients
need 2 weeks (calendar days 1 to 5, and 8 to 12 excluding weekends). The first
patient is young and needs 2 hours of lunch break. One doctor ('lakare') is
unavailable on day 1 between 8-12 and day 2 between 15-16. Moreover, 'fysioterap'
is unavailable on day 1 between 8-12. The doctor's unavailability is
incorporated into the schedule.

Solution status: Optimal
nb_admitted_patients = 3

Patient  p1 schedule:
---------------------------------
(1, '0800', 'pedagog', 45)
(1, '0900', 'arbetsterap', 45)
(1, '1000', 'psykolog', 45)
(1, '1300', 'logoped', 45)
(1, '1430', 'lakare', 30)
(1, '1515', 'fysioterap', 45)
(2, '0800', 'arbetsterap', 120)
(2, '1015', 'logoped', 45)
(2, '1300', 'pedagog', 45)
(2, '1400', 'psykolog', 45)
(2, '1500', 'fysioterap', 45)
(3, '0800', 'fysioterap', 45)
(3, '0930', 'logoped', 45)
(3, '1300', 'pedagog', 45)
(3, '1400', 'psykolog', 45)
(3, '1500', 'arbetsterap', 45)

Patient  p2 schedule:
---------------------------------
(1, '0800', 'arbetsterap', 45)
(1, '0900', 'logoped', 45)
(1, '1000', 'pedagog', 45)
(1, '1115', 'fysioterap', 45)
(1, '1300', 'psykolog', 45)
(2, '0800', 'fysioterap', 45)
(2, '0900', 'logoped', 45)
(2, '1015', 'arbetsterap', 45)
(2, '1115', 'psykolog', 45)
(2, '1345', 'pedagog', 45)
(3, '0815', 'pedagog', 45)
(3, '0915', 'fysioterap', 45)
(3, '1015', 'logoped', 45)
(3, '1115', 'arbetsterap', 45)
(3, '1300', 'psykolog', 45)
(8, '0800', 'psykolog', 45)
(8, '0900', 'logoped', 45)
(8, '1000', 'fysioterap', 45)
(8, '1115', 'arbetsterap', 45)
(8, '1500', 'pedagog', 45)
(9, '0800', 'pedagog', 45)
(9, '0900', 'psykolog', 45)
(9, '1015', 'logoped', 45)
(9, '1115', 'fysioterap', 45)
(9, '1300', 'arbetsterap', 120)
(9, '1515', 'lakare', 30)
(10, '0815', 'pedagog', 45)
(10, '0915', 'logoped', 45)
(10, '1100', 'fysioterap', 45)
(10, '1300', 'arbetsterap', 120)
(10, '1515', 'psykolog', 45)

Patient  p3 schedule:
---------------------------------
(1, '0845', 'pedagog', 45)
(1, '0945', 'fysioterap', 45)
(1, '1045', 'arbetsterap', 45)
(1, '1400', 'psykolog', 45)
(1, '1500', 'logoped', 45)
(2, '0800', 'logoped', 45)
(2, '0915', 'psykolog', 45)
(2, '1015', 'pedagog', 45)
(2, '1115', 'fysioterap', 45)
(2, '1515', 'arbetsterap', 45)
(3, '0800', 'arbetsterap', 120)
(3, '1015', 'psykolog', 45)
(3, '1115', 'logoped', 45)
(3, '1315', 'fysioterap', 45)
(3, '1415', 'pedagog', 45)
(8, '0800', 'fysioterap', 45)
(8, '0900', 'lakare', 30)
(8, '0945', 'pedagog', 45)
(8, '1045', 'psykolog', 45)
(8, '1300', 'arbetsterap', 120)
(8, '1515', 'logoped', 45)
(9, '0800', 'logoped', 45)
(9, '0900', 'pedagog', 45)
(9, '1000', 'fysioterap', 45)
(9, '1100', 'arbetsterap', 45)
(9, '1430', 'psykolog', 45)
(10, '0845', 'fysioterap', 45)
(10, '1015', 'pedagog', 45)
(10, '1115', 'logoped', 45)
(10, '1330', 'psykolog', 45)
(10, '1500', 'arbetsterap', 45)