from typing import Dict, Any, List, Optional

from realm_keeper.models.game_object import GameObject


class GameWorld:
    def __init__(self):
        self.objects: Dict[str, GameObject] = {}
        self.rules: List[str] = []

    def add_object(self, obj: GameObject):
        self.objects[obj.id] = obj

    def get_object(self, object_id: str) -> Optional[GameObject]:
        return self.objects.get(object_id)

    def add_rule(self, rule: str):
        self.rules.append(rule)

    def get_state(self) -> Dict[str, Any]:
        state = {
            "objects": {},
            "rules": self.rules
        }
        for id, obj in self.objects.items():
            obj_state = obj.dict()
            obj_state['equipment'] = {slot: equip.dict() for slot, equip in obj.equipment.items()}
            state["objects"][id] = obj_state
        return state
