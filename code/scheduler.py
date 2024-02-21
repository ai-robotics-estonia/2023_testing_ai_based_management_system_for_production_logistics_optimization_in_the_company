from datetime import datetime, timedelta
from copy import copy, deepcopy
from .helpers import p

#..['accessible'] - can access location with given restrictions
#.. prediction_worker - time from history, static calculations and ML models

def brain_v0_2(self):
    try:
        holder = []
        self.create_arr() # creates lists of available resources
        for b in self.beacons_arr: #available beacons
            for wt in self.work_task_arr: #available tasks
                if b['transport_type'] == wt['transport_type']: # correct system
                    result = self.beacons_worker.beacons[b['beacon_id']].path_worker.get_connection(b['anchor_id'],
                                                                                                    wt['anchor_id'])
                    if result['accessible'] is True:
                        p = self.pos_worker.prediction_worker.get_estimated({'beacon_id': b['beacon_id'],
                                                                             'type': 'ba',
                                                                             'anchor_id_start': b['anchor_id'],
                                                                             'anchor_id_end': wt['anchor_id']
                                                                             }, 'slim')
                        holder.append({'time': p,
                                       'work_task_id': wt['work_task_id'],
                                       'mission_id': wt['mission_id'],
                                       'anchor_id': wt['anchor_id'],
                                       'beacon_id': b['beacon_id'],
                                       'status': 'WT_BUFFER'})

        holder = sorted(holder, key=lambda d: d['time'])
        #look over all result
        while len(holder) > 0:
            o = holder[0]
            self.activate_work_tasks.append(o)
            holder = [item for item in holder if
                      item['work_task_id'] != o['work_task_id'] and item['beacon_id'] != o['beacon_id']]
        # new tasks will be started and monitored after this
    except Exception as e:
        p(e)

def generate_schedule_list(self):
    try:

        self.create_schedule() # creates lists of available resources
        holder = {'active_list': deepcopy(self.active_list),
                  'scheduler_list': [],
                  'index': 0,
                  'next_task': None}
        if len(self.work_task_scheduler) == 0:
            self.scheduled_list = holder['scheduler_list']

            # Nohting to schedule
            return
        else:
            while len(self.beacons_schedule) > 0 and len(holder['scheduler_list']) < 20 and holder['index'] < 100:
                holder['index'] += 1

                self.beacons_schedule.sort(key=lambda x: x['estimated_end'], reverse=False)
                b = self.beacons_schedule[0]
                if b['work_task_id'] is not None:
                    # sai tehtud ja liidame koguse
                    self.work_task_scheduler[b['work_task_id']]['active'] = False
                    self.scheduler_actions(b['work_task_id'], 'add')

                holder['next_task'] = None

                for wt_id in self.work_task_scheduler:
                    if self.work_task_scheduler[wt_id]['active'] == False:
                        prediction = self.pos_worker.prediction_worker.get_estimated({'type': 'work_task',
                                                                                      'id': wt_id,
                                                                                      'beacon_id': b['beacon'].id},
                                                                                     'full')
                        if prediction['calculated']['result']['accessible']:
                            # can access start

                            if self.beacons_worker.beacons[b['beacon'].id].beacon.anchor_force_id is not None:
                                fa = self.beacons_worker.beacons[b['beacon'].id].path_worker.get_connection(
                                    b['last_anchor_id'],
                                    self.beacons_worker.beacons[b['beacon'].id].beacon.anchor_force_id)

                                fa['time'] = self.pos_worker.prediction_worker.get_estimated({'beacon_id': b['beacon'].id,
                                                                                              'type': 'ba',
                                                                                              'anchor_id_start': b['last_anchor_id'],
                                                                                              'anchor_id_end': self.beacons_worker.beacons[
                                                                                                  b['beacon'].id].beacon.anchor_force_id
                                                                                              }, 'slim')
                                r = self.beacons_worker.beacons[b['beacon'].id].path_worker.get_connection(
                                    self.beacons_worker.beacons[b['beacon'].id].beacon.anchor_force_id,
                                    prediction['calculated']['result']['anchor_list'][0])

                                r['time'] = self.pos_worker.prediction_worker.get_estimated({'beacon_id': b['beacon'].id,
                                                                                             'type': 'ba',
                                                                                             'anchor_id_start': self.beacons_worker.beacons[
                                                                                                 b['beacon'].id].beacon.anchor_force_id,
                                                                                             'anchor_id_end': prediction['calculated']['result'][
                                                                                                 'anchor_list'][0]
                                                                                             }, 'slim')
                            else:
                                fa = {'time': 0,
                                      'accessible': True}
                                r = self.beacons_worker.beacons[b['beacon'].id].path_worker.get_connection(
                                    b['last_anchor_id'],
                                    prediction['calculated']['result']['anchor_list'][0])
                                r['time'] = self.pos_worker.prediction_worker.get_estimated({'beacon_id': b['beacon'].id,
                                                                                             'type': 'ba',
                                                                                             'anchor_id_start': b['last_anchor_id'],
                                                                                             'anchor_id_end': prediction['calculated']['result'][
                                                                                                 'anchor_list'][0]
                                                                                             }, 'slim')
                            if r['accessible'] is True and fa['accessible'] is True:
                                start_time = b['estimated_end']
                                if start_time < datetime.utcnow():
                                    start_time = datetime.utcnow()
                                new_start = start_time + timedelta(seconds=r['time']) + timedelta(seconds=fa['time'])
                                if holder['next_task'] is None or holder['next_task']['estimated_start'] > new_start:
                                    t = prediction['calculated']['result']['result'] + (
                                            float(prediction['calculated']['result']['stops']) * float(
                                        self.pos_worker.setting_obj['POS_LOAD_TIME']))
                                    holder['next_task'] = {
                                        'estimated_start': new_start,
                                        'work_task_id': wt_id,
                                        'last_anchor_id': prediction['calculated']['result']['anchor_list'][-1],
                                        'duration': t,
                                    }

                if holder['next_task'] is not None:
                    wt_id = holder['next_task']['work_task_id']
                    holder['next_task']['done_quantity'] = self.work_task_scheduler[wt_id]['done_quantity']
                    holder['next_task']['quantity_per_run'] = self.work_task_scheduler[wt_id]['quantity_per_run']
                    holder['next_task']['work_task_name'] = self.work_tasks_worker.work_tasks[wt_id].work_task.name,
                    holder['next_task']['beacon_id'] = b['beacon'].id
                    holder['next_task']['status'] = 'ESTIMATED'
                    holder['next_task']['estimated_end'] = holder['next_task']['estimated_start'] + timedelta(
                        seconds=holder['next_task']['duration'])
                    holder['next_task'] = self.set_extra_attr(holder['next_task'])
                    if holder['next_task']['done_quantity'] + holder['next_task']['quantity_per_run'] > self.work_task_scheduler[wt_id][
                        'quantity']:
                        holder['next_task']['quantity_per_run'] = self.work_task_scheduler[wt_id]['quantity'] - holder['next_task'][
                            'done_quantity']
                    holder['scheduler_list'].append(copy(holder['next_task']))

                    self.beacons_schedule[0]['work_task_id'] = wt_id
                    self.beacons_schedule[0]['estimated_end'] = holder['next_task']['estimated_end']

                    self.work_task_scheduler[wt_id]['active'] = True
                else:
                    self.beacons_schedule = self.beacons_schedule[1:]

            self.scheduled_list = holder['scheduler_list']
    except Exception as e:
        p(e)
