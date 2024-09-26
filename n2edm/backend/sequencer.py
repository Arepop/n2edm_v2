from .items import ScheduleItem


class Sequencer:
    preambule = []
    number_of_cycles = 0

    def __init__(self):
        self.commands_list = []
        self.pre_sequence = []
        self.main_sequence = []
        self.post_sequence = []

    def decode(self):
        self.commands_list = []
        self.sequence = []
        self.pre_sequence = []
        self.main_sequence = []
        self.post_sequence = []

        for schedule_item in ScheduleItem.all():

            if schedule_item.sequence == "pre":
                self.pre_sequence.append(
                    (
                        schedule_item.start_time,
                        schedule_item.set_item.initial_scpi_command,
                        schedule_item.set_item.params,
                    )
                )
                self.pre_sequence.append(
                    (
                        schedule_item.stop_time,
                        schedule_item.set_item.final_scpi_command,
                        schedule_item.set_item.params,
                    )
                )

            if schedule_item.sequence == "main":
                self.main_sequence.append(
                    (
                        schedule_item.start_time,
                        schedule_item.set_item.initial_scpi_command,
                        schedule_item.set_item.params,
                    )
                )
                self.main_sequence.append(
                    (
                        schedule_item.stop_time,
                        schedule_item.set_item.final_scpi_command,
                        schedule_item.set_item.params,
                    )
                )

            if schedule_item.sequence == "post":
                self.post_sequence.append(
                    (
                        schedule_item.start_time,
                        schedule_item.set_item.initial_scpi_command,
                        schedule_item.set_item.params,
                    )
                )
                self.post_sequence.append(
                    (
                        schedule_item.stop_time,
                        schedule_item.set_item.final_scpi_command,
                        schedule_item.set_item.params,
                    )
                )
        # for schedule_item in Infinitschedule_itemObject.all():

        #     if schedule_item.sequence == "pre":
        #         self.pre_sequence.append(
        #             (
        #                 schedule_item.start_time,
        #                 schedule_item.set_item.initial_scpi_command,
        #                 schedule_item.set_item.params,
        #             )
        #         )

        #     if schedule_item.sequence == "main":
        #         self.main_sequence.append(
        #             (
        #                 schedule_item.start_time,
        #                 schedule_item.set_item.initial_scpi_command,
        #                 schedule_item.set_item.params,
        #             )
        #         )

        #     if schedule_item.sequence == "post":
        #         self.post_sequence.append(
        #             (
        #                 schedule_item.start_time,
        #                 schedule_item.set_item.initial_scpi_command,
        #                 schedule_item.set_item.params,
        #             )
        #         )

        self.pre_sequence.sort(key=self.sort_criteria)
        self.main_sequence.sort(key=self.sort_criteria)
        self.post_sequence.sort(key=self.sort_criteria)

        if len(self.pre_sequence) != 0:

            h = self.pre_sequence[0][0]

        else:
            h = self.main_sequence[0][0]

        self.pre_sequence.append((0, "ITERATOR", "Iterator init", 0))
        self.main_sequence.insert(0, (self.main_sequence[0][0], "LABEL", "Label", 0))
        self.main_sequence.append((self.main_sequence[-1][0], "IF", "if", 0))
        self.main_sequence.append((self.main_sequence[-1][0], "GOTO", "goto", 0))
        self.main_sequence.append((self.main_sequence[-1][0], "ELIF", "ELIF", 0))
        self.main_sequence.append((self.main_sequence[-1][0], "ENDIF", "endif", 0))

        self.commands_list.extend(self.pre_sequence)
        self.commands_list.extend(self.main_sequence)
        self.commands_list.extend(self.post_sequence)

        it = 1
        lab = "A"
        # if h != 0:

        # self.sequence.append(
        # ',:sequencer:AddSeqLine 0,"SLEEP' + " " + str(h) + '"\n'
        # )

        for line in self.commands_list:

            if line[1] == "ITERATOR":
                self.sequence.append(':sequencer:AddSeqLine 0,"SET iterator' + str(it) + ' = 0"\n')

                self.sequence.append(':sequencer:AddSeqLine 0,"SET stop_timecondition = FALSE\n')

                self.sequence.append(':sequencer:AddSeqLine 0,"SET trigtimestamp=0"\n')
                self.sequence.append("\n")

            elif line[1] == "LABEL":

                self.sequence.append(':sequencer:AddSeqLine 0,"LABEL LABEL' + lab + '"\n')

                self.sequence.append(':sequencer:AddSeqLine 0,"IF $(stop_timecondition)"\n')

                self.sequence.append(':sequencer:AddSeqLine 0,"GOTO stop_time\n')

                self.sequence.append(':sequencer:AddSeqLine 0,"ELSE"\n')

                self.sequence.append(':sequencer:AddSeqLine 0,"ENDIF"\n')

                self.sequence.append(':sequencer:AddSeqLine 0,"SEND :lasttrigger:getTS?"\n')

                self.sequence.append(':sequencer:AddSeqLine 0,"EVALI time=$(trigtimestamp)\n')

            elif line[1] == "IF":
                self.sequence.append(
                    ':sequencer:AddSeqLine 0,"EVALI iterator'
                    + str(it)
                    + " = $(iterator"
                    + str(it)
                    + ') 1 +" \n'
                )

                if self.number_of_cycles == -1:
                    une = ' >="\n'
                else:
                    une = ' <="\n'
                self.sequence.append(
                    ':sequencer:AddSeqLine 0,"EVALI condition = $(iterator'
                    + str(it)
                    + ") "
                    + str(self.number_of_cycles)
                    + une
                )

                self.sequence.append(':sequencer:AddSeqLine 0,"IF $(condition)"\n')

            elif line[1] == "GOTO":
                self.sequence.append(':sequencer:AddSeqLine 0,"GOTO LABEL' + lab + '"\n')

            elif line[1] == "ELIF":
                self.sequence.append(':sequencer:AddSeqLine 0,"ELIF"\n')

            elif line[1] == "ENDIF":
                self.sequence.append(':sequencer:AddSeqLine 0,"ENDIF"\n\n')

                self.sequence.append(':sequencer:AddSeqLine 0,"LABEL stop_time"\n')

            else:

                if line[0] != h:
                    self.sequence.append(
                        ':sequencer:AddSeqLine 0,"EVALI'
                        + " time=$(time) "
                        + str(abs(line[0] - int(h)))
                        + ' +"\n'
                    )
                    h = line[0]

                if line[2] != None:
                    self.sequence.append(
                        ':sequencer:AddSeqLine 0,"SEND'
                        + " "
                        + str(line[1])
                        + ","
                        + str(line[2])
                        + ',$(time)"\n'
                    )

                else:
                    self.sequence.append(
                        ':sequencer:AddSeqLine 0,"SEND' + " " + str(line[1]) + ',$(time)"\n'
                    )

        return self.sequence

    def sort_criteria(self, command):
        # TODO: set sort criteria to command[3]
        return command[0]

    @classmethod
    def set_number_of_cycles(cls, n_of_cycles):
        cls.number_of_cycles = n_of_cycles
        return n_of_cycles
