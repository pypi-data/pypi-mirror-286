import emoji
import itertools
from tqdm import trange, tqdm
from colorama import Fore, Style


class Render:
    def __init__(self):
        """
        Initialize the class by giving default values.
        """
        self.total = 0
        self.prog_bar = None
        # Loading animation characters
        self.loading_animation = itertools.cycle(['|', '/', '-', '\\'])
        print('Contacting the server to run the tests...')

    def create_progress_bar(self, job_id, total):    
        self.total_cases = total
        print('Initializing job with job_id:', Style.BRIGHT + job_id + Style.RESET_ALL)
        print('We are going to run',
            Style.BRIGHT + f'{self.total_cases}' + Style.RESET_ALL,
            'test cases.\n')
        
        self.prog_bar = trange(
            self.total_cases,
            desc='\ Testing in progress: ',
            ncols=100,
            ascii=' =',
            bar_format=Style.BRIGHT + Fore.BLUE + '{desc} [{bar}] {percentage:3.0f}%' + Style.RESET_ALL)

    def progress_bar_loading(self):
        # Get the next character in the loading animation
        animation_char = next(self.loading_animation)
        self.prog_bar.set_description(f'{animation_char} Testing in progress')

    def print_progress_bar(self, case_id, case_name, status): 
        success = Fore.GREEN + f'{status}' + Style.RESET_ALL
        failed = Fore.RED + f'{status}' + Style.RESET_ALL
        status_message = success if status else failed
        tqdm.write(
            Style.DIM +    
            f"Test case {case_id}: {case_name} -- "
            + Style.RESET_ALL +
            status_message
        )
        self.prog_bar.update(1)

    def close(self, is_success):
        self.prog_bar.close()
        if is_success:
            print(Fore.GREEN + Style.BRIGHT +
                '\n\nAll tests passed successfully, Congratulations! '
                + Style.RESET_ALL
                + emoji.emojize(":winking_face_with_tongue:")
                + emoji.emojize(":grinning_face_with_smiling_eyes:")  
                + '\n'  
            )
        else:   
            print(Fore.RED + Style.BRIGHT +
                '\n\nOne of the tests failed. Sorry! '
                + Style.RESET_ALL
                + emoji.emojize(":face_with_symbols_on_mouth:")
                + emoji.emojize(":face_with_symbols_on_mouth:")  
                + '\n'  
            )
        

