Optimization code for doctor/patient scheduling

A sample schedule obtained from the optimizer looks as follows:

(calendar_day, time, visit_duration)
---------------------------------------------------------------
The following is a solution obtained from an input file with 3 patients.

Solution status: Optimal
nb_admitted_patients =  3

Patient  p1 schedule:
---------------------------------
(1, '0815', 'psykolog', 45)
(1, '1115', 'logoped', 45)
(1, '1500', 'arbetsterap', 45)
(2, '0830', 'pedagog', 45)
(2, '0945', 'psykolog', 45)
(2, '1315', 'logoped', 45)
(2, '1415', 'fysioterap', 45)
(3, '1430', 'pedagog', 45)
(4, '0830', 'fysioterap', 45)
(4, '1300', 'pedagog', 45)
(4, '1400', 'arbetsterap', 45)
(4, '1500', 'psykolog', 45)
(5, '0830', 'fysioterap', 45)
(5, '0945', 'arbetsterap', 120)
(5, '1345', 'logoped', 45)
(5, '1515', 'lakare', 30)

Patient  p2 schedule:
---------------------------------
(1, '0915', 'logoped', 45)
(1, '1300', 'fysioterap', 45)
(1, '1445', 'psykolog', 45)
(2, '0845', 'logoped', 45)
(2, '1315', 'lakare', 30)
(2, '1500', 'arbetsterap', 45)
(3, '1300', 'logoped', 45)
(3, '1400', 'arbetsterap', 120)
(4, '1100', 'fysioterap', 45)
(4, '1300', 'arbetsterap', 45)
(4, '1415', 'psykolog', 45)
(4, '1515', 'logoped', 45)
(5, '0815', 'arbetsterap', 45)
(5, '0930', 'pedagog', 45)
(5, '1115', 'psykolog', 45)
(8, '0915', 'fysioterap', 45)
(8, '1330', 'psykolog', 45)
(8, '1515', 'pedagog', 45)
(9, '0800', 'pedagog', 45)
(9, '1030', 'logoped', 45)
(9, '1445', 'fysioterap', 45)
(10, '0845', 'fysioterap', 45)
(10, '1015', 'psykolog', 45)
(10, '1345', 'pedagog', 45)
(10, '1515', 'logoped', 45)
(11, '0800', 'arbetsterap', 120)
(11, '1100', 'pedagog', 45)
(12, '0800', 'psykolog', 45)
(12, '0915', 'fysioterap', 45)
(12, '1015', 'pedagog', 45)
(12, '1115', 'arbetsterap', 45)

Patient  p3 schedule:
---------------------------------
(1, '1045', 'pedagog', 45)
(1, '1400', 'psykolog', 45)
(2, '0830', 'arbetsterap', 120)
(2, '1300', 'pedagog', 45)
(2, '1415', 'logoped', 45)
(2, '1515', 'fysioterap', 45)
(3, '0900', 'psykolog', 45)
(3, '1315', 'fysioterap', 45)
(4, '0900', 'pedagog', 45)
(4, '1000', 'fysioterap', 45)
(5, '0900', 'arbetsterap', 45)
(5, '1045', 'logoped', 45)
(5, '1415', 'psykolog', 45)
(8, '1000', 'psykolog', 45)
(8, '1300', 'logoped', 45)
(8, '1400', 'fysioterap', 45)
(8, '1515', 'arbetsterap', 45)
(9, '0845', 'pedagog', 45)
(10, '0945', 'logoped', 45)
(10, '1115', 'arbetsterap', 45)
(10, '1430', 'psykolog', 45)
(11, '1115', 'logoped', 45)
(11, '1415', 'arbetsterap', 45)
(12, '0800', 'arbetsterap', 120)
(12, '1030', 'fysioterap', 45)
(12, '1300', 'logoped', 45)
(12, '1400', 'pedagog', 45)
(12, '1500', 'lakare', 30)

