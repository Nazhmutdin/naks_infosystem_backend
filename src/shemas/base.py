from pydantic import BaseModel, ConfigDict


class BaseShema(BaseModel):

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        validate_assignment=True,
        revalidate_instances="always"
    )
    
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, type(self)):
            return False
        
        self_dict = self.model_dump()

        for key, value in other.model_dump().items():
            if key == "ident": continue
            
            if key not in self_dict:
                return False
            
            if value != self_dict[key]:
                return False
        
        return True

