from abc import ABC, abstractmethod


class LineupConstraints(object):
    def __init__(self):
        self._constraints = []
        self._banned = set()
        self._locked = set()

    def __iter__(self):
        return ConstraintIterator(self._constraints)

    def __len__(self):
        return len(self._constraints)

    def __repr__(self):
        return '<LineupConstraintSet: ' + \
                ', '.join([repr(c) for c in self._constraints]) + \
                ', <Banned: {}'.format(repr(self._banned)) + '>' + \
                ', <Locked: {}'.format(repr(self._locked)) + '>' + \
                '>'

    def __str__(self):
        return '\n'.join(str(c) for c in self._constraints) + \
               'BANNED:\n' + \
               '\n'.join(['\t{}'.format(str(p) for p in self._banned)]) + \
               'LOCKED:\n' + \
               '\n'.join(['\t{}'.format(str(p) for p in self._locked)])

    def __eq__(self, constraintset):
        if len(self._constraints) != len(constraintset._constraints):
            return False

        if set(self._constraints) != set(constraintset._constraints):
            return False

        if self._locked != constraintset._locked:
            return False

        if self._banned != constraintset._banned:
            return False

        return True

    def __contains__(self, player):
        if player in self._locked:
            return True

        if player in self._banned:
            return True

        for c in self._constraints:
            if isinstance(c, PlayerGroupConstraint):
                if player in c.players:
                    return True

    # TODO this will create conflicts with exposure code, maybe create
    # a new class for players locked/banned by the exposure code?
    def _check_conflicts(self, constraint):
        if isinstance(constraint, PlayerGroupConstraint):
            for p in constraint.players:
                if p in self._locked or p in self._banned:
                    raise ConstraintConflictException('Ban/lock constraint ' +
                                                      'for {} '.format(p) +
                                                      'already exists')

    def _add(self, constraint):
        self._check_conflicts(constraint)

        if constraint not in self._constraints:
            self._constraints.append(constraint)
        else:
            raise ConstraintConflictException('Duplicate constraint')

    def add_group_constraint(self, players, bound):
        self._add(PlayerGroupConstraint(players, bound))

    def ban(self, players):
        if len(players) == 0:
            raise ConstraintException('Empty ban group')

        for p in players:
            if p in self:
                raise ConstraintConflictException('{}'.format(p) + 'exists in' +
                                                  'another constraint')

        self._banned.update(players)

    def lock(self, players):
        if len(players) == 0:
            raise ConstraintException('Empty lock group')

        for p in players:
            if p in self:
                raise ConstraintConflictException('{}'.format(p) + 'exists in' +
                                                  'another constraint')
        self._locked.update(players)


class ConstraintConflictException(Exception):
    pass


class ConstraintIterator(object):
    def __init__(self, constraints):
        self._constraints = constraints
        self.ndx = 0

    def __next__(self):
        if self.ndx >= len(self._constraints):
            raise StopIteration

        r = self._constraints[self.ndx]
        self.ndx += 1
        return r


class AbstractConstraint(ABC):
    @abstractmethod
    def __init__(self):
        super().__init__()

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __eq__(self, constraint):
        pass

    @abstractmethod
    def __hash__(self):
        pass

    @abstractmethod
    def __contains__(self, player):
        pass

    @abstractmethod
    def apply(self):
        pass


class ConstraintException(Exception):
    pass


class PlayerConstraint(AbstractConstraint):
    def __init__(self, players):
        if not len(players):
            raise ConstraintException('No players in group')

        if len(players) != len(set(players)):
            raise ConstraintException('Duplicate players in group')

        self.players = players

        super().__init__()

    def __eq__(self, rule):
        return set(self.players) == set(rule.players)

    def __hash__(self):
        return hash(''.join(sorted(self.players)))

    def __contains__(self, player):
        return player in self.players


class PlayerGroupConstraint(PlayerConstraint):
    def __init__(self, players, bound):
        super().__init__(players)
        self.exact = None
        self.lo = None
        self.hi = None

        if isinstance(bound, (list,tuple)) and len(bound) == 2:
            self.lo = bound[0]
            self.hi = bound[1]
            self._hi_lo_bounds_sanity_check()
        elif isinstance(bound, int):
            self.exact = bound
            self._exact_bounds_sanity_check()
        else:
            raise ConstraintException('Bound must be length 2 or int')

    def __repr__(self):
        return '<PlayerGroupConstraint: {} of {}>'.format(self._bounds_str,
                                                          self.players)

    def __str__(self):
        ls = ['Using {} of:'.format(self._bounds_str)] + \
             ['\t'+p for p in self.players]
        return '\n'.join(ls)

    def __eq__(self, constraint):
        return super().__eq__(constraint) and self.exact == constraint.exact \
               and self.lo == constraint.lo and self.hi == constraint.hi

    def __hash__(self):
        return hash((super().__hash__(), self.exact, self.lo, self.hi))

    @property
    def _bounds_str(self):
        if self.exact:
            return '{0.exact}'.format(self)

        return '{0.lo} to {0.hi}'.format(self)

    def _exact_bounds_sanity_check(self):
        if self.exact <= 0:
            raise ConstraintException('Exact bound may not less than or ' +
                                      'equal to zero')
        if self.exact >= len(self.players):
            raise ConstraintException('Exact bound may not be greater than ' +
                                      'or equal number of players in group')

    def _hi_lo_bounds_sanity_check(self):
        if self.lo < 1:
            raise ConstraintException('Lower bound for {!r} '.format(self) +
                                      'cannot be less than 1')
        if self.hi == self.lo:
            raise ConstraintException('Lower bound for {!r} '.format(self) +
                                      'cannot equal upper bound')
        if self.hi < self.lo:
            raise ConstraintException('Upper bound for {!r} '.format(self) +
                                      'cannot be less than lower bound.')
        if self.hi > len(self.players) or self.lo > len(self.players):
            raise ConstraintException('Bound for {!r} cannot '.format(self) +
                                      'be greater than number of players in ' +
                                      'group')

    def apply(self):
        pass
