import fqr


class Pet(fqr.Object):
    """A pet."""

    id_: fqr.Field[str]
    _alternate_id: fqr.Field[str]

    name: fqr.Field[str]
    type: fqr.Field[str]
    in_: fqr.Field[str]
    is_tail_wagging: fqr.Field[bool] = True
