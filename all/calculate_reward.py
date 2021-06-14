# Actions
DO_NOTHING = 'do_nothing'
ALLOW_TO_ENTER = 'allow_to_enter'
CALL_TO_DOCTOR = 'call_to_doctor'
BUILD_PATH = 'build_path'
BUILD_EVAC_PATH = 'build_evac_path'
CALL_TO_POLICE = 'call_to_police'

# Actions map from 0 to 5
ACTIONS_MAP = [DO_NOTHING, ALLOW_TO_ENTER, CALL_TO_DOCTOR, BUILD_PATH, CALL_TO_POLICE]


def calculate_all_reward(df, action):
    action = ACTIONS_MAP[action]

    hour = df['hour'].values * 24
    worker_arrived = df['workerArrived'].values
    stranger_arrived = df['strangerArrived'].values
    ill_worker_arrived = df['illWorkerArrived'].values
    worker_fell = df['workerFell'].values
    worker_stand_up = df['workerStandUp'].values
    build_path = df['buildPath'].values
    emergency_start = df['emergencyStart'].values

    if 8 <= hour[1] < 20:
        if worker_arrived[1] and action == ALLOW_TO_ENTER:
            return 1000

        if worker_arrived[1] and action == ALLOW_TO_ENTER:
            return -1000

        if stranger_arrived[1] and action == ALLOW_TO_ENTER:
            return -1000

        if ill_worker_arrived[1] and action == ALLOW_TO_ENTER:
            return -1000

        if worker_fell[0] and action == CALL_TO_DOCTOR and not worker_stand_up[1]:
            return 5000

        if worker_fell[0] and action != CALL_TO_DOCTOR and not worker_stand_up[1]:
            return -5000

        if build_path[1] and action == BUILD_PATH:
            return 3000

        if build_path[1] and action != BUILD_PATH:
            return -1000

        if emergency_start[1] and action == CALL_TO_POLICE:
            return 15000

        if emergency_start[1] and action != CALL_TO_POLICE:
            return -15000

    return 0
