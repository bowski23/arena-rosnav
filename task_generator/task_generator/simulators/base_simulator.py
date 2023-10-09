import os
from typing import Callable, Collection, Dict, Optional

from task_generator.shared import ModelType, ObstacleProps, PositionOrientation, Position, Robot


class BaseSimulator:

    _namespace: str
    _ns_prefix: Callable[..., str]
    _spawn_model: Dict[ModelType, Callable]

    def __init__(self, namespace: str):
        self._namespace = namespace
        self._ns_prefix = lambda *topic: os.path.join(self._namespace, *topic)
        self._spawn_model = dict()

    @property
    def MODEL_TYPES(self) -> Collection[ModelType]:
        return self._spawn_model.keys()

    def spawn_model(self, model_type: ModelType, *args, **kwargs):
        if model_type in self._spawn_model:
            return self._spawn_model[model_type](*args, **kwargs)

        raise NotImplementedError(f"{type(self).__name__} does not implement spawn_model[{model_type}]")

    def before_reset_task(self):
        """
        Is executed each time before the task is reseted. This is useful in
        order to pause the simulation.
        """
        raise NotImplementedError()

    def after_reset_task(self):
        """
        Is executed after the task is reseted. This is useful to unpause the
        simulation.
        """
        raise NotImplementedError()

    def remove_all_obstacles(self):
        """
        Removes all obstacles from the current simulator. Does not remove
        the robot!
        """
        raise NotImplementedError()

    def spawn_random_dynamic_obstacle(self, **args):
        """
        Spawn a single random dynamic obstacle.

        Args:
            position: [int, int, int] denoting the x, y and angle.
            min_radius: minimal radius of the obstacle
            max_radius: maximal radius of the obstacle
            linear_vel: linear velocity
            angular_vel_max: maximal angular velocity
        """
        raise NotImplementedError()

    def spawn_random_static_obstacles(self, **args):
        """
        Spawn a single random static obstacle.

        Args:
            position: [int, int, int] denoting the x, y and angle.
            min_radius: minimal radius of the obstacle
            max_radius: maximal radius of the obstacle
        """
        raise NotImplementedError()

    def publish_goal(self, goal: Position):
        """
        Publishes the goal. 
        """
        raise NotImplementedError()

    def move_robot(self, pos: PositionOrientation, name: Optional[str] = None):
        """
        Move the robot to the given position. 
        """
        raise NotImplementedError()

    def spawn_robot(self, robot: Robot):
        """
        Spawn a robot in the simulator.
        A position is not specified because the robot is moved at the 
        desired position anyway.
        """
        raise NotImplementedError()

    def spawn_obstacle(self, obs: ObstacleProps) -> str:
        raise NotImplementedError()

    def delete_obstacle(self, obstacle_id: str):
        raise NotImplementedError()
