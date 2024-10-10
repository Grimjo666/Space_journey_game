import pygame
from collections import defaultdict

FPS_STEP_COUNTER = 0


class BaseScene:
    def __init__(self, screen):
        self.active = True
        self.screen = screen

        self.time_running = False
        self.start_time = pygame.time.get_ticks()
        self.time = 0

        self.run_create_objects = True

    @staticmethod
    def trigger_event(event):
        repeat_event = pygame.event.Event(event)
        pygame.event.post(repeat_event)

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def start(self):
        self.active = True

    def scene(self):
        if self.run_create_objects:
            self.create_objects()
            self.run_create_objects = False

        if self.active:
            self.update()
            self.draw()

    def stop(self):
        self.active = False
        self.time_running = False

    def create_objects(self):
        pass

    def setting_up_objects(self):
        pass


class SceneManager:
    def __init__(self, scenes=None):
        """
        :param scenes: dict. Сцены, имеют приоритет по расположению,
         последняя сцена в словаре будет рисоваться поверх остальных
        """
        if scenes:
            if isinstance(scenes, dict):
                self.scenes = scenes
            else:
                raise ValueError(f'Аргумент scenes должен быть dict, а передаётся {type(scenes)}')

        self.scenes = {}
        self.current_scene = None
        self.running = True

    def add_scene(self, name, scene, active=True):
        """
        При добавлении новой сцены, она получает приоритет при рендеринге (если она активна)
        :param name:
        :param scene:
        :param active: Если передать False, то сцены будут добавляться выключенными
        :return:
        """
        if isinstance(scene, BaseScene):
            self.scenes[name] = scene

            if not active:
                self.scenes[name].stop()
        else:
            raise ValueError(f'Аргумент scene не является сценой, а передаётся {type(scene)}')

    def get_scene(self, name):
        return self.scenes[name]

    def stop_all(self):
        for scene in self.scenes.values():
            scene.stop()

    def handle_events(self, event):
        for scene in self.scenes.values():
            if scene.active:
                scene.handle_event(event)

    def draw_scenes(self):
        for scene in self.scenes.values():
            if scene.active:
                scene.scene()


class Grid:
    """Класс, являющийся системой хранения объектов в сцене."""
    def __init__(self, world_scale, cell_size):
        self.cell_size = cell_size
        self.grid_width = world_scale[0] // cell_size
        self.grid_height = world_scale[1] // cell_size
        self.cells = defaultdict(list)
        self.hash_objs = {}

    def add_object(self, obj):
        """Добавляем объект в нужную ячейку сетки."""
        x, y = obj.body.position
        cell = (int(x // self.cell_size), int(y // self.cell_size))

        # Если объект есть в хэше, проверяем, остался ли он в своей ячейке или нет
        old_cell = self.hash_objs.get(obj)
        if old_cell and old_cell != cell:
            self.cells[old_cell].remove(obj)

        # Обновляем хэш и добавляем объект в новую ячейку
        self.hash_objs[obj] = cell
        self.cells[cell].append(obj)

    def update(self):
        """Обновляем позиции всех объектов в сетке."""
        for obj in self.get_all_obj():
            x, y = obj.body.position
            cell = (int(x // self.cell_size), int(y // self.cell_size))
            if self.hash_objs.get(obj) != cell:
                self.add_object(obj)

    def remove(self, obj):
        """Удаляем объект из сетки."""
        cell = self.hash_objs.get(obj)
        if cell and obj in self.cells[cell]:
            self.cells[cell].remove(obj)
            del self.hash_objs[obj]  # Удаляем объект из хэша

    def get_neighboring_objects(self, obj):
        """Возвращает объекты из ячейки с текущим объектом и соседних ячеек."""
        x, y = obj.body.position
        cell_x = int(x // self.cell_size)
        cell_y = int(y // self.cell_size)

        neighboring_objects = []

        # Перебираем соседние ячейки (включая текущую)
        for dx in range(-1, 2):  # -1, 0, 1 - сдвиг по оси X
            for dy in range(-1, 2):  # -1, 0, 1 - сдвиг по оси Y
                neighbor_cell = (cell_x + dx, cell_y + dy)
                neighboring_objects.extend(self.cells[neighbor_cell])

        return neighboring_objects

    def get_all_obj(self):
        """Возвращает все объекты из всех ячеек."""
        return (obj for objs_array in self.cells.values() for obj in objs_array)

