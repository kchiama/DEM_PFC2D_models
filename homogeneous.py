#Import commands
import itasca as it
from itasca import ballarray as ba
import os, stat, csv, math
import shutil as sh
from shutil import copytree, ignore_patterns
import sys
import datetime
from datetime import datetime

#Python state is not cleared by the model new or model restore commands:
it.command("python-reset-state false")
#Define source code folder as src
src = "d:/dem/Dense_5m/"
#Destination folders of files are defined in each of the for-loops as dst

now=datetime.now()
now_formatted = now.strftime("%m-%d-%y_%H.%M.%S")
errors_filename=src+str(now_formatted+'_errors_log.txt')

with open(errors_filename, 'w') as file_object: # make new file
    file_object.write("FILES THAT BUGGED: \n")
print('define file error')

# Homogeneous Sediment Trials
coh_ten_matrix = [[1e5,1e5],[5e5,5e5],[10e5,10e5],[15e5,15e5],[20e5,20e5]]
dip_degrees = [20,40,60]
FS_lengths = [0.25,0.50,0.75] 
print('define parameters')

for ct in coh_ten_matrix:
    g_pre_growth_pb_coh = ct[0]
    g_pre_growth_pb_ten = ct[1]
    for g_fault_dip_deg in dip_degrees:
        for fault_seed_length in FS_lengths:
            it.command("""
            model new
            program thread auto
            model restore 'unbonded'

            program log on
            program log-file 'simulation_log.txt'
            [io.out('BEGINNING')]

            program call 'parameter_def.p2dat' suppress
            program call 'fish_functions.p2fis' suppress
            ;plot 'particles' active on
            ;plot 'contacts' active on
            plot 'particles' movie index 1 interval 500 
            plot 'contacts' movie index 1 interval 500 
                
            @allParameters
                contact model linearpbond range contact type 'ball-ball'
                contact method deformability emod 1e9 kratio 1.0 range contact type 'ball-ball'
                contact method pb_deformability emod 1e9 kratio 1.0 range contact type 'ball-ball'
                contact property pb_ten {coh} pb_coh {coh} pb_rmul @g_pb_rmul dp_nratio @g_dp_nratio pb_fa @g_pb_fa range contact type 'ball-ball'
                contact property lin_force 0.0 0.0 lin_mode 1 range contact type 'ball-ball'
                ball attribute force-contact multiply 0.0 moment-contact multiply 0.0
                ball attribute displacement multiply 0.0
                contact method bond gap @g_pre_growth_bond_gap range contact type 'ball-ball'
                ball property 'fric' @g_pre_growth_ball_friction
            @settlement
            @saveCurrentModelState('homogeneous_bonded')
            @setstrongwallfriction
            ;@makeFault                 
                wall create ...
                    vertices ...
                    @g_x_piece_1_limit @g_y_model_begin ...
                    [g_x_piece_1_limit - g_fault_slip * (math.cos({dip_deg} * math.degrad))] [g_y_model_begin - g_fault_slip * (math.sin({dip_deg} * math.degrad))] ...
                    name @g_fault_wall_name ...
                    id @g_fault_wall_id
            @setWallFriction(@g_fault_wall_id, @g_fault_friction)
                wall create vertices ...
                    [g_x_piece_1_limit - 1 * math.cos({dip_deg} * math.degrad) - 0.05] [g_y_model_begin - 1 * math.sin({dip_deg} * math.degrad) + 0.05] ...
                    [(g_x_piece_1_limit - 1 * math.cos({dip_deg} * math.degrad)) - g_fault_measure_size * math.cos(({dip_deg} - 90) * math.degrad) - 0.05] [(g_y_model_begin - 1 * math.sin({dip_deg} * math.degrad)) - g_fault_measure_size * math.sin(({dip_deg} - 90) * math.degrad) + 0.05] ...
                    name @g_fault_measure_1_name ...
                    id @g_fault_measure_1_id
                wall create vertices ...
                    [g_x_piece_1_limit - 2 * math.cos({dip_deg} * math.degrad) - 0.05] [g_y_model_begin - 2 * math.sin({dip_deg} * math.degrad) + 0.05] ...
                    [(g_x_piece_1_limit - 2 * math.cos({dip_deg} * math.degrad)) - g_fault_measure_size * math.cos(({dip_deg} - 90) * math.degrad) - 0.05] [(g_y_model_begin - 2 * math.sin({dip_deg} * math.degrad)) - g_fault_measure_size * math.sin(({dip_deg} - 90) * math.degrad) + 0.05] ...
                    name @g_fault_measure_2_name ...
                    id @g_fault_measure_2_id
                wall create vertices ...
                    [g_x_piece_1_limit - 3 * math.cos({dip_deg} * math.degrad) - 0.05] [g_y_model_begin - 3 * math.sin({dip_deg} * math.degrad) + 0.05] ...
                    [(g_x_piece_1_limit - 3 * math.cos({dip_deg} * math.degrad)) - g_fault_measure_size * math.cos(({dip_deg} - 90) * math.degrad) - 0.05] [(g_y_model_begin - 3 * math.sin({dip_deg} * math.degrad)) - g_fault_measure_size * math.sin(({dip_deg} - 90) * math.degrad) + 0.05] ... 
                    name @g_fault_measure_3_name ...
                    id @g_fault_measure_3_id
                wall create vertices ...
                    [g_x_piece_1_limit - 4 * math.cos({dip_deg} * math.degrad) - 0.05] [g_y_model_begin - 4 * math.sin({dip_deg} * math.degrad) + 0.05] ...
                    [(g_x_piece_1_limit - 4 * math.cos({dip_deg} * math.degrad)) - g_fault_measure_size * math.cos(({dip_deg} - 90) * math.degrad) - 0.05] [(g_y_model_begin - 4 * math.sin({dip_deg} * math.degrad)) - g_fault_measure_size * math.sin(({dip_deg} - 90) * math.degrad) + 0.05] ... 
                    name @g_fault_measure_4_name ...
                    id @g_fault_measure_4_id
                wall create vertices ...
                    [g_x_piece_1_limit - 5 * math.cos({dip_deg} * math.degrad) - 0.05] [g_y_model_begin - 5 * math.sin({dip_deg} * math.degrad) + 0.05] ...
                    [(g_x_piece_1_limit - 5 * math.cos({dip_deg} * math.degrad)) - g_fault_measure_size * math.cos(({dip_deg} - 90) * math.degrad) - 0.05] [(g_y_model_begin - 5 * math.sin({dip_deg} * math.degrad)) - g_fault_measure_size * math.sin(({dip_deg} - 90) * math.degrad) + 0.05] ... 
                    name @g_fault_measure_5_name ...
                    id @g_fault_measure_5_id
                fracture create position (@g_x_piece_1_limit,@g_y_model_begin) dip [180 - {dip_deg}] size [2*(g_pre_growth_total_thickness / (math.sin({dip_deg} * math.degrad))) * {FS}]
                fracture property 'sj_kn' 1e9 'sj_ks' 1e9 'sj_fric' 0.1 'sj_coh' 0.0 'sj_ten' 0.0 'sj_large' 1 ;'sj_radius' [g_width_fault_seed] 'sj_rmul' [g_pb_rmul] 
                fracture contact-model model 'smoothjoint' install dist [g_width_fault_seed] activate
            ;@settlement
            wall group @g_all_moving_walls_group_name ...
                range id-list @g_fault_wall_id @g_vertical_wall_x_begin_id @g_horizonal_wall_y_begin_part_near_x_begin_id @g_fault_measure_1_id @g_fault_measure_2_id @g_fault_measure_3_id @g_fault_measure_4_id @g_fault_measure_5_id
            wall attribute velocity-x [g_wall_velocity_norm * math.cos({dip_deg} * math.degrad)] range group @g_all_moving_walls_group_name
            wall attribute velocity-y [g_wall_velocity_norm * math.sin({dip_deg} * math.degrad)] range group @g_all_moving_walls_group_name
            """.format(coh = g_pre_growth_pb_coh, ten = g_pre_growth_pb_ten, dip_deg = g_fault_dip_deg, FS = fault_seed_length))
            ##switch to python
            print('deformation sequence')
            try:
                ## switch to pfc
                it.command("""
                ;@runFixDeformation
                @resetMechanicalTime
                @activateExportResultDuringDeformation
                @saveCurrentModelState('deformation_state_0m')
                """) 
                positions = ba.pos() 
                fields = ['X', 'Y']
                rows = positions
                filename = "Particle_Positions_coh{coh:.1e}_ten{ten:.1e}_dip{dip_deg}_FS{FS}_0slip.csv".format(coh = g_pre_growth_pb_coh, ten = g_pre_growth_pb_ten, dip_deg = g_fault_dip_deg, FS = fault_seed_length) #format name to scientific :.2e
                with open(filename, 'w', newline='') as csvfile: 
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(fields)
                    csvwriter.writerows(rows)
                it.command("""
                        model mechanical timestep fix 3e-5
                        model solve time [g_deformation_1m / nb_deformation_steps]
                    @saveCurrentModelState('deformation_state_0,5m')
                """)
                print('0.5 m')
                positions = ba.pos() 
                fields = ['X', 'Y']
                rows = positions
                filename = "Particle_Positions_coh{coh:.1e}_ten{ten:.1e}_dip{dip_deg}_FS{FS}_0,5slip.csv".format(coh = g_pre_growth_pb_coh, ten = g_pre_growth_pb_ten, dip_deg = g_fault_dip_deg, FS = fault_seed_length) #format name to scientific :.2e
                with open(filename, 'w', newline='') as csvfile: 
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(fields)
                    csvwriter.writerows(rows)
                it.command("""
                        model solve time [g_deformation_1m / nb_deformation_steps]
                    @saveCurrentModelState('deformation_state_1m')
                """)
                print('1.0 m')
                positions = ba.pos() 
                fields = ['X', 'Y']
                rows = positions
                filename = "Particle_Positions_coh{coh:.1e}_ten{ten:.1e}_dip{dip_deg}_FS{FS}_1slip.csv".format(coh = g_pre_growth_pb_coh, ten = g_pre_growth_pb_ten, dip_deg = g_fault_dip_deg, FS = fault_seed_length) #format name to scientific :.2e
                with open(filename, 'w', newline='') as csvfile: 
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(fields)
                    csvwriter.writerows(rows)
                it.command("""
                        model solve time [g_deformation_1m / nb_deformation_steps]
                    @saveCurrentModelState('deformation_state_1,5m')
                """)   
                print('1.5 m')
                positions = ba.pos() 
                fields = ['X', 'Y']
                rows = positions
                filename = "Particle_Positions_coh{coh:.1e}_ten{ten:.1e}_dip{dip_deg}_FS{FS}_1,5slip.csv".format(coh = g_pre_growth_pb_coh, ten = g_pre_growth_pb_ten, dip_deg = g_fault_dip_deg, FS = fault_seed_length) #format name to scientific :.2e
                with open(filename, 'w', newline='') as csvfile: 
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(fields)
                    csvwriter.writerows(rows)
                it.command("""
                        model solve time [g_deformation_1m / nb_deformation_steps]
                    @saveCurrentModelState('deformation_state_2m')
                """)
                print('2.0 m')
                positions = ba.pos() 
                fields = ['X', 'Y']
                rows = positions
                filename = "Particle_Positions_coh{coh:.1e}_ten{ten:.1e}_dip{dip_deg}_FS{FS}_2slip.csv".format(coh = g_pre_growth_pb_coh, ten = g_pre_growth_pb_ten, dip_deg = g_fault_dip_deg, FS = fault_seed_length) #format name to scientific :.2e
                with open(filename, 'w', newline='') as csvfile: 
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(fields)
                    csvwriter.writerows(rows)
                it.command("""
                        model solve time [g_deformation_1m / nb_deformation_steps]
                    @saveCurrentModelState('deformation_state_2,5m')
                """)
                print('2.5 m')
                positions = ba.pos() 
                fields = ['X', 'Y']
                rows = positions
                filename = "Particle_Positions_coh{coh:.1e}_ten{ten:.1e}_dip{dip_deg}_FS{FS}_2,5slip.csv".format(coh = g_pre_growth_pb_coh, ten = g_pre_growth_pb_ten, dip_deg = g_fault_dip_deg, FS = fault_seed_length) #format name to scientific :.2e
                with open(filename, 'w', newline='') as csvfile: 
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(fields)
                    csvwriter.writerows(rows)
                it.command("""
                        model solve time [g_deformation_1m / nb_deformation_steps]
                    @saveCurrentModelState('deformation_state_3m')
                """)
                print('3.0 m')
                positions = ba.pos() 
                fields = ['X', 'Y']
                rows = positions
                filename = "Particle_Positions_coh{coh:.1e}_ten{ten:.1e}_dip{dip_deg}_FS{FS}_3slip.csv".format(coh = g_pre_growth_pb_coh, ten = g_pre_growth_pb_ten, dip_deg = g_fault_dip_deg, FS = fault_seed_length) #format name to scientific :.2e
                with open(filename, 'w', newline='') as csvfile: 
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(fields)
                    csvwriter.writerows(rows)
                it.command("""
                        model solve time [g_deformation_1m / nb_deformation_steps]
                    @saveCurrentModelState('deformation_state_3,5m')
                """)
                print('3.5 m')
                positions = ba.pos() 
                fields = ['X', 'Y']
                rows = positions
                filename = "Particle_Positions_coh{coh:.1e}_ten{ten:.1e}_dip{dip_deg}_FS{FS}_3,5slip.csv".format(coh = g_pre_growth_pb_coh, ten = g_pre_growth_pb_ten, dip_deg = g_fault_dip_deg, FS = fault_seed_length) #format name to scientific :.2e
                with open(filename, 'w', newline='') as csvfile: 
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(fields)
                    csvwriter.writerows(rows)
                it.command("""
                        model solve time [g_deformation_1m / nb_deformation_steps]
                    @saveCurrentModelState('deformation_state_4m')
                """)
                print('4.0 m')
                positions = ba.pos() 
                fields = ['X', 'Y']
                rows = positions
                filename = "Particle_Positions_coh{coh:.1e}_ten{ten:.1e}_dip{dip_deg}_FS{FS}_4slip.csv".format(coh = g_pre_growth_pb_coh, ten = g_pre_growth_pb_ten, dip_deg = g_fault_dip_deg, FS = fault_seed_length) #format name to scientific :.2e
                with open(filename, 'w', newline='') as csvfile: 
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(fields)
                    csvwriter.writerows(rows)
                it.command("""
                        model solve time [g_deformation_1m / nb_deformation_steps]
                    @saveCurrentModelState('deformation_state_4,5m')
                """)
                print('4.5 m')
                positions = ba.pos() 
                fields = ['X', 'Y']
                rows = positions
                filename = "Particle_Positions_coh{coh:.1e}_ten{ten:.1e}_dip{dip_deg}_FS{FS}_4,5slip.csv".format(coh = g_pre_growth_pb_coh, ten = g_pre_growth_pb_ten, dip_deg = g_fault_dip_deg, FS = fault_seed_length) #format name to scientific :.2e
                with open(filename, 'w', newline='') as csvfile: 
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(fields)
                    csvwriter.writerows(rows)
                it.command("""
                        model solve time [g_deformation_1m / nb_deformation_steps]
                    @saveCurrentModelState('deformation_state_5m')
                """)
                print('5.0 m')
                positions = ba.pos() 
                fields = ['X', 'Y']
                rows = positions
                filename = "Particle_Positions_coh{coh:.1e}_ten{ten:.1e}_dip{dip_deg}_FS{FS}_5slip.csv".format(coh = g_pre_growth_pb_coh, ten = g_pre_growth_pb_ten, dip_deg = g_fault_dip_deg, FS = fault_seed_length) #format name to scientific :.2e
                with open(filename, 'w', newline='') as csvfile: 
                    csvwriter = csv.writer(csvfile)
                    csvwriter.writerow(fields)
                    csvwriter.writerows(rows)
                it.command("""
                        ; Solve to an equilibrium state again
                        wall attribute velocity-x 0.0
                        wall attribute velocity-y 0.0
                ;@settlement
                @saveCurrentModelState('last_deformation_stage')
                [io.out('END')]
                project save
                program return
                """)
                #switch to python
            except Exception as trial_error:
                print("trial error: ",trial_error)
                with open(errors_filename, 'a') as file_object: # make new file
                    file_object.write(trial_error)
                    file_object.write(", ")
                    file_object.write(coh)
                    file_object.write(", ")
                    file_object.write(ten)
                    file_object.write(", ")
                    file_object.write(dip)
                    file_object.write(", ")
                    file_object.write(FS)
                    file_object.write("\n")
            positions = ba.pos() #get all of the particle positions from ballarray
            #x,y = positions.T #transpose x and y locations into individual variables
            fields = ['X', 'Y']
            rows = positions
            filename = "Particle_Positions_coh{coh:.1e}_ten{ten:.1e}_dip{dip_deg}_FS{FS}_final.csv".format(coh = g_pre_growth_pb_coh, ten = g_pre_growth_pb_ten, dip_deg = g_fault_dip_deg, FS = fault_seed_length) #format name to scientific :.2e
            with open(filename, 'w', newline='') as csvfile: 
                csvwriter = csv.writer(csvfile)                   
                csvwriter.writerow(fields)
                csvwriter.writerows(rows)
            #Copy all files to new directory except guidebug.txt (error)
            dst = "d:/dem/Homogeneous_Results7/D5_coh{coh:.1e}_ten{ten:.1e}_dip{dip_deg}_FS{FS}".format(coh = g_pre_growth_pb_coh, ten = g_pre_growth_pb_ten, dip_deg = g_fault_dip_deg, FS = fault_seed_length)
            sh.copytree(src,dst, ignore=ignore_patterns('guidebug*'))
            #Delete everything that ends in .png or .csv
            png_files = os.listdir(src)
            png_filtered_files = [file for file in png_files if file.endswith(".png")]
            for file in png_filtered_files: 
                path_to_file1 = os.path.join(src, file)
                os.remove(path_to_file1)
            csv_files = os.listdir(src)
            csv_filtered_files = [file for file in csv_files if file.endswith(".csv")]
            for file in csv_filtered_files: 
                path_to_file2 = os.path.join(src, file)
                os.remove(path_to_file2)
            result_files = os.listdir(src)
            result_filtered_files = [file for file in result_files if file.endswith(".result")]
            for file in result_filtered_files: 
                path_to_file2 = os.path.join(src, file)
                os.remove(path_to_file2)