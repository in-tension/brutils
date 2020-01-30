## TODO: also make archetype_all_elems
## and achetype_only_universal_elems

from .misc import is_hashable

class CollectionArchetypeBuilder :
    """
    """


    # def __init__(self, *args, arch_perc_thresh=0.5, extra_string='added', missing_string='missing') :
    def __init__(self, arch_perc_thresh=0.5, extra_string='added', missing_string='missing', *args) :
        """ arch_perc_thresh -> archetype percent threshold
                percent of collections that must contain a specific element for the element to go into the archetype

            extra_string
                string used as key in an archetype_deviation dict when the collection in question has extra elements that are in the archetype

            missing_string
                string used as key in an archetype_deviation dict when the collection in question is missing elements that are in the archetype
        """
        if len(args) == 0 :
            self.collections_ = {}
        elif len(args) == 1 :
            self.collections_ = args[0]
        else :
            self.collections_ = args

        self.arch_perc_thresh = arch_perc_thresh
        self.extra_string = extra_string
        self.missing_string = missing_string



    def add_collection(self, collection_name, collection_) :
        """ """
        self.collections_[collection_name] = collection_


    def create_collection_elem_counts(self) :
        self.collection_elem_counts = {}

        for collection_ in self.collections_.values() :
            for elem in collection_ :
                if not is_hashable(elem) :
                    raise TypeError('CollectionArchetypeBuilder:all elements of each collection must be hashable')
                if elem in self.collection_elem_counts :
                    self.collection_elem_counts[elem] += 1
                else :
                    self.collection_elem_counts[elem] = 1

        return self.collection_elem_counts


    def create_archetype(self) :

        self.create_collection_elem_counts()

        self.archetype = set()
        self.archetype_inclusive = set()
        self.archetype_exclusive = set()

        cnt_thresh = len(self.collections_) * self.arch_perc_thresh
        exclusive_thresh = len(self.collections_)

        for elem, cnt in self.collection_elem_counts.items() :
            self.archetype_inclusive.add(elem)
            if cnt >= cnt_thresh :
                self.archetype.add(elem)
            if cnt >= exclusive_thresh :
                self.archetype_exclusive.add(elem)


        return self.archetype

    def create_archetype_deviations(self) :
        self.create_archetype()

        self.archetype_deviations = {}

        for name, collection_ in self.collections_.items() :
            collection_as_set = set(collection_)

            deviation = {}

            extra = collection_as_set - self.archetype
            missing = self.archetype - collection_as_set

            if len(extra) > 0 :
                deviation[self.extra_string] = list(extra)

            if len(missing) > 0 :
                deviation[self.missing_string] = list(missing)

            self.archetype_deviations[name] = deviation

        return self.archetype_deviations

    def create_all(self) :
        self.create_archetype_deviations()

    def get_archetype_info(self, archetype_ver='') :
        """
        archetype_ver='' returns archetype  ## can actually be any string that isn't 'inclusive' or 'exclusive'
        archetype_ver='inclusive' returns archetype_inclusive
        archetype_ver='exclusive' returns archetype_exclusive
        """
        self.create_archetype_deviations()
        if archetype_ver == 'inclusive' :
            archetype_to_return = self.archetype_inclusive
        elif archetype_er == 'exclusive' :
            archetype_to_return = self.archetype_exclusive
        else :
            archetype_to_return = self.archetype

        return archetype_to_return, self.archetype_deviations


def make_and_get_archytype(*args, **kwargs) :
    archetype_builder = CollectionArchetypeBuilder(*args, **kwargs)
    return archetype_builder.get_archetype_info()
    # archetype = archetype_builder.create_archetype()
    # archetype_deviations = archetype_builder.create_archetype_deviations()
    #
    # return archetype, archetype_deviations
