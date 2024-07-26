from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from .....Internal.ArgSingleList import ArgSingleList
from .....Internal.ArgSingle import ArgSingle
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RtypeCls:
	"""Rtype commands group definition. 1 total commands, 0 Subgroups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._cmd_group = CommandsGroup("rtype", core, parent)

	def set(self, periodicity: enums.SrsPeriodicity, offset: int = None) -> None:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:SRS:RTYPe \n
		Snippet: driver.configure.nrSubMeas.srs.rtype.set(periodicity = enums.SrsPeriodicity.SL1, offset = 1) \n
		Defines the SRS periodicity at slot level. \n
			:param periodicity: Periodicity of the SRS transmissions in slots.
			:param offset: Number of slots, shifting the start of the SRS slot sequence.
		"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('periodicity', periodicity, DataType.Enum, enums.SrsPeriodicity), ArgSingle('offset', offset, DataType.Integer, None, is_optional=True))
		self._core.io.write(f'CONFigure:NRSub:MEASurement<Instance>:SRS:RTYPe {param}'.rstrip())

	# noinspection PyTypeChecker
	class RtypeStruct(StructBase):
		"""Response structure. Fields: \n
			- Periodicity: enums.SrsPeriodicity: Periodicity of the SRS transmissions in slots.
			- Offset: int: Number of slots, shifting the start of the SRS slot sequence."""
		__meta_args_list = [
			ArgStruct.scalar_enum('Periodicity', enums.SrsPeriodicity),
			ArgStruct.scalar_int('Offset')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Periodicity: enums.SrsPeriodicity = None
			self.Offset: int = None

	def get(self) -> RtypeStruct:
		"""SCPI: CONFigure:NRSub:MEASurement<Instance>:SRS:RTYPe \n
		Snippet: value: RtypeStruct = driver.configure.nrSubMeas.srs.rtype.get() \n
		Defines the SRS periodicity at slot level. \n
			:return: structure: for return value, see the help for RtypeStruct structure arguments."""
		return self._core.io.query_struct(f'CONFigure:NRSub:MEASurement<Instance>:SRS:RTYPe?', self.__class__.RtypeStruct())
