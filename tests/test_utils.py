from path_explorator import PathGoesBeyondLimits

from exceptions.exc import NotAUserId
from utils import Logger, PathCutter, PathJoiner, PathValidEnsurer

from config import STORAGE_PATH

logger = Logger()
cutter = PathCutter()
joiner = PathJoiner(STORAGE_PATH)
ensurer = PathValidEnsurer(STORAGE_PATH)

def test_cutter():
    failure = False
    expected_path = '/folder/file.txt'
    tmplt = expected_path
    paths = [f'/5{tmplt}', f'/321{tmplt}', f'/5039{tmplt}', f'/59438729{tmplt}']
    invalid_paths = [f'/foo{tmplt}', f'/f312oo{tmplt}', f'/21foo{tmplt}', f'/foo123{tmplt}', f'/1f2f3f4o5o{tmplt}']
    for path in paths:
        cut_path = cutter.cut_user_id_from_storage_path(path)
        assert cut_path == expected_path
    for invalid_path in invalid_paths:
        try:
            cutter.cut_user_id_from_storage_path(invalid_path)
            failure = True # если схавал невалидный путь и не поднял исключение
        except NotAUserId:
            pass
    assert failure == False

def test_joiner_join_with_root_path():
    path_to_dir = 'very/cool/dir'
    joined_path_to_dir = joiner.join_with_root_path(path_to_dir)
    expected_path_to_dir = f'{STORAGE_PATH}/{path_to_dir}'
    assert joined_path_to_dir == expected_path_to_dir
    path_to_file = 'very/cool/dir/file.txt'
    joined_path_to_file = joiner.join_with_root_path(path_to_file)
    expected_path_to_file = f'{STORAGE_PATH}/{path_to_file}'
    assert  joined_path_to_file == expected_path_to_file

def test_joiner_create_absolute_path():
    user_id_int = 1
    user_id_str = '1'
    path_to_dir = 'very/cool/dir'
    abs_path_dir_int_id = joiner.create_absolute_path(user_id_int, path_to_dir)
    abs_path_dir_str_id = joiner.create_absolute_path(user_id_str, path_to_dir)
    expected_path_to_dir = f'{STORAGE_PATH}/{user_id_str}/{path_to_dir}'
    assert abs_path_dir_str_id == abs_path_dir_int_id == expected_path_to_dir
    path_to_file = 'very/cool/dir/file.txt'
    abs_path_file_int_id = joiner.create_absolute_path(user_id_int, path_to_file)
    abs_path_file_str_id = joiner.create_absolute_path(user_id_str, path_to_file)
    expected_path_to_file = f'{STORAGE_PATH}/{user_id_str}/{path_to_file}'
    assert  abs_path_file_str_id == abs_path_file_int_id == expected_path_to_file

def test_ensurer_goes_beyond_limits():
    beyond_path = '/home'
    beyond_rel_path = f'{ensurer.root}/../../dir'
    safe_path = f'{ensurer.root}/very/cool/dir'
    is_unsafe = ensurer.is_goes_beyond_limits(beyond_path)
    is_unsafe_rel = ensurer.is_goes_beyond_limits(beyond_rel_path)
    is_safe = not ensurer.is_goes_beyond_limits(safe_path)
    assert is_unsafe == is_unsafe_rel == is_safe == True
