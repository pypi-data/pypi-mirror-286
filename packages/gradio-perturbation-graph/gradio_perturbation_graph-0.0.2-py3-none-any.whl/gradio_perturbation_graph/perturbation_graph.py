from __future__ import annotations

from typing import Any, Callable

from gradio.components.base import Component
from gradio.events import Events

from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
import json
import io
import base64

class perturbation_graph(Component):
    """
    Creates a very simple textbox for user to enter string input or display string output.
    """
    
    def getLigandImg(ligand) -> Any:
        # 从SMILES字符串创建分子
        mol = Chem.MolFromMolFile(ligand)
        AllChem.Compute2DCoords(mol)
        return Draw.MolToImage(mol)       

    EVENTS = [
        Events.input,
        Events.change,
        Events.submit,
        Events.like,
    ]

    

    def handleData(self, data) -> Any:
        data = json.loads(data.replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t'))
        ligands = data['ligands']

        def getLigandImg(ligand) -> Any:
            # 从SMILES字符串创建分子
            mol = Chem.MolFromMolBlock(ligand)
            AllChem.Compute2DCoords(mol)
            img = Draw.MolToImage(mol)  
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
            return img_base64

        for item in ligands:
            item['img'] = getLigandImg(item['content'])

        final = {
            "ligands": ligands,
            "pairs": data['pairs']
        }
        return json.dumps(final)

    def __init__(
        self,
        value: str | Callable | None = None,
        *,
        placeholder: str | None = None,
        label: str | None = None,
        every: float | None = None,
        show_label: bool | None = None,
        scale: int | None = None,
        min_width: int = 160,
        interactive: bool | None = None,
        visible: bool = True,
        rtl: bool = False,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        render: bool = True,
        key: int | str | None = None,
    ):
        """
        Parameters:
            value: default text to provide in textbox. If callable, the function will be called whenever the app loads to set the initial value of the component.
            placeholder: placeholder hint to provide behind textbox.
            label: component name in interface.
            every: If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute.
            show_label: if True, will display label.
            scale: relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.
            min_width: minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.
            interactive: if True, will be rendered as an editable textbox; if False, editing will be disabled. If not provided, this is inferred based on whether the component is used as an input or output.
            visible: If False, component will be hidden.
            rtl: If True and `type` is "text", sets the direction of the text to right-to-left (cursor appears on the left of the text). Default is False, which renders cursor on the right.
            elem_id: An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.
            elem_classes: An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.
            render: If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.
            key: if assigned, will be used to assume identity across a re-render. Components that have the same key across a re-render will have their value preserved.
        """
        self.rtl = rtl

        # 在这里对输入做预处理，把ligand的图生成出来

        
        placeholder = self.handleData(placeholder)
        self.placeholder = placeholder
        super().__init__(
            label=label,
            every=every,
            show_label=show_label,
            scale=scale,
            min_width=min_width,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            value=value,
            render=render,
            key=key,
            load_fn=None,
        )

    def preprocess(self, payload: str | None) -> str | None:
        """
        Parameters:
            payload: the text entered in the textarea.
        Returns:
            Passes text value as a {str} into the function.
        """
        print('Preprocess')
        return None if payload is None else str(payload)

    def postprocess(self, value: str | None) -> str | None:
        """
        Parameters:
            value: Expects a {str} returned from function and sets textarea value to it.
        Returns:
            The value to display in the textarea.
        """
        print('Postprocess')
        return None if value is None else str(value)

    def api_info(self) -> dict[str, Any]:
        return {"type": "string"}

    def example_payload(self) -> Any:
        return "Hello!!"

    def example_value(self) -> Any:
        return "Hello!!"
    
    def update(self, placeholder: str) -> any:
        placeholder = self.handleData(placeholder)
        self.placeholder = placeholder
        print('update', self.FRONTEND_DIR)
        # self.__init__(self, placeholder)
        res = {}
        res['placeholder'] = placeholder
        return res
