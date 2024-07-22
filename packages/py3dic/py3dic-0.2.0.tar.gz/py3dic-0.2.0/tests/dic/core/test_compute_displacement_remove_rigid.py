
import numpy as np
import pytest

from py3dic.dic import GridSize
from py3dic.dic.core.core_calcs import compute_disp_and_remove_rigid_transform



def test_compute_disp_and_remove_rigid_transform_null(dic_result_file_container_fixture):
    point_list = dic_result_file_container_fixture.pointlist
    image_list = dic_result_file_container_fixture.imagelist
    # win_size = dic_result_file_container_fixture.get_winsize()

    i = 0
    disp0= compute_disp_and_remove_rigid_transform(new_points=point_list[i], old_points=point_list[0])
    expected = [(0, 0)]*9
    np.testing.assert_array_equal(disp0, expected)
    

def test_compute_disp_and_remove_rigid_transform(dic_result_file_container_fixture):

    point_list = dic_result_file_container_fixture.pointlist
    image_list = dic_result_file_container_fixture.imagelist
    # win_size = dic_result_file_container_fixture.get_winsize()

    i = 1
    disp0= compute_disp_and_remove_rigid_transform(new_points=point_list[i], old_points=point_list[0])
    expected = [(-2.9072876, -0.32419586),
            (-3.2105408, -0.35385132),
            (-3.4964905, -0.3884735),
            (-2.9302368, -0.02923584),
            (-2.6487122, -0.067489624),
            (0.029693604, -0.1701355),
            (5.243164, 0.60565186),
            (4.647888, 0.3896637),
            (5.272461, 0.33818054)]
    np.testing.assert_allclose(disp0, expected, 
        rtol=1e-5, atol=1e-5)
    
    i = 2
    expected = [(-2.9717712, -0.30542755),
            (-3.2428894, -0.37127686),
            (-3.4962769, -0.42736816),
            (-2.9659119, -0.0070266724),
            (-2.662201, -0.08300781),
            (0.03488159, -0.21360779),
            (5.28891, 0.6858902),
            (4.691162, 0.3982544),
            (5.324188, 0.323349)]
    np.testing.assert_allclose(
        compute_disp_and_remove_rigid_transform(new_points=point_list[i], old_points=point_list[0]), 
        expected,
        rtol=1e-5, atol=1e-5)
    
    i = 3
    expected = [(-2.4072876, 0.032577515),
            (-2.9313965, -1.2674103),
            (-1.5014648, -2.0356903),
            (-5.364502, 0.3045807),
            (-1.7254944, -0.16412354),
            (-1.6682129, -0.7373352),
            (4.7734375, 1.960556),
            (3.5157776, 1.1108551),
            (7.3092957, 0.79600525)]
    np.testing.assert_allclose(
        compute_disp_and_remove_rigid_transform(new_points=point_list[i], old_points=point_list[0]), 
        expected,
        rtol=1e-5, atol=1e-5)
    


def test_compute_displacement_remove_rigid_ag():
    """ this is a test for the compute_displacement_remove_rigid function using 
    an artificially (predictable) generated field)

    """
    gs = GridSize(xmin=0, xmax=1, ymin=0, ymax=1, xnum=11, ynum=11, win_size_x=20, win_size_y=20)
    gs.prepare_gridXY()
    # prepare displacement field
    def disp_field(t, gs): 
        time_factor = 0.1
        disp_x = np.log(time_factor *t+1)*np.log10(gs.grid_x * gs.grid_y + 1) * np.sqrt(gs.grid_x * gs.grid_y) * np.arctan2(gs.grid_x, gs.grid_y)
        disp_y = np.log(time_factor*t+1)*np.log(gs.grid_x * gs.grid_y + 1) * np.sqrt(gs.grid_x * gs.grid_y) * np.arctan2(gs.grid_y, gs.grid_x)
        return disp_x, disp_y

    # create a displacement field
    t= 1
    disp_x, disp_y = disp_field(t=t, gs=gs)
    # disp_field_flat = GridSize.grid_to_flat_array(disp_x, disp_y)
    
    # calculate initial and final coordinates
    coordinates = np.column_stack([gs.grid_x.ravel(), gs.grid_y.ravel()])
    new_coordinates = coordinates + np.column_stack([disp_x.ravel(), disp_y.ravel()])

    disp_func  = np.array(compute_disp_and_remove_rigid_transform(coordinates, new_coordinates))

    low, hi, avg, std, val = -0.03920131384294878, 0.01269876864066849, 2.575992679037295e-16, 0.009530325102166816, 0.007489919505741682
    assert pytest.approx(disp_func.min(), abs=1e-15) == low, f"t={t} : min value not the same"
    assert pytest.approx(disp_func.max(), abs=1e-15) == hi, f"t={t} :max value not the same"
    assert pytest.approx(disp_func.mean(), abs=1e-15) == avg, f"t={t} :avg value not the same"
    assert pytest.approx(disp_func.std(), abs=1e-15) == std, f"t={t} :std value not the same"
    assert pytest.approx(disp_func[2,1], abs=1e-15) == val, f"t={t} :specific value not the same"
