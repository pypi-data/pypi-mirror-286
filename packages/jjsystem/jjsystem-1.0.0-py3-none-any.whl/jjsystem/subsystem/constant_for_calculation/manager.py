from jjsystem.common.subsystem import operation, manager
from jjsystem.subsystem.constant_for_calculation.resource \
    import ConstantForCalculation
from jjsystem.subsystem.application.resource import Application
from jjsystem.common.subsystem.pagination import Pagination


class List(operation.List):

    def do(self, session, **kwargs):
        query = session.query(ConstantForCalculation). \
            join(Application, Application.id == # noqa
                 ConstantForCalculation.application_id)
        query = self.manager.apply_filters(
            query, ConstantForCalculation, **kwargs)
        query = query.distinct()

        dict_compare = {"application.": Application}
        query = self.manager.apply_filters_includes(
            query, dict_compare, **kwargs)
        query = query.distinct()

        total_rows = None
        if self.manager.with_pagination(**kwargs):
            total_rows = query.count()

        pagination = Pagination.get_pagination(
            ConstantForCalculation, **kwargs)
        if pagination.order_by is not None:
            pagination.adjust_order_by(ConstantForCalculation)
        query = self.driver.apply_pagination(query, pagination)
        result = query.all()

        return (result, total_rows)


class Manager(manager.Manager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.list = List(self)
