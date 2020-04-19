# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------------------------

from cifo.algorithm.genetic_algorithm import GeneticAlgorithm
from cifo.custom_problem.portfolio_investment_problem import (
    PortfolioInvestmentProblem, input_space_red_pip
)
from cifo.problem.objective import ProblemObjective
from cifo.algorithm.ga_operators import (
    initialize_using_random,
    roulettewheel_selection, rank_selection, tournament_selection,
    pip_crossover,
    swap_mutation, insert_mutation, inversion_mutation, scramble_mutation,
    elitism_replacement, standard_replacement 
)

from cifo.util.terminal import Terminal, FontColor
from cifo.util.observer import LocalSearchObserver
from random import randint
import numpy as np
from copy import deepcopy

from os import listdir, path, mkdir
from os.path import isfile, join
from pandas import pandas as pd
from pandas import read_excel


# Problem
#--------------------------------------------------------------------------------------------------
# Decision Variables

closing_prices = read_excel(r".\data\sp_12_weeks.xlsx")  # importing data example
#closing_prices = closing_prices.iloc[:, :10]

def get_dv_pip(prices):
    est_ret = np.log(prices.values[1:] / prices.values[:-1])  # returns for each period in column
    exp_ret = np.sum(est_ret, axis=0)  # expected return over time interval
    cov_ret = np.cov(est_ret, rowvar=False)  # estimated covariance matrix over time interval
    return exp_ret, cov_ret

pip_constraints = {
    "Risk-Tolerance": 1,
    "Budget": 100000
}

# Configuration
#--------------------------------------------------------------------------------------------------
parent_selection = roulettewheel_selection

# dictionaries to create test directories
valid_Init = {initialize_using_random: "rand"}

valid_Select = {roulettewheel_selection: "rol", tournament_selection: "tourn", rank_selection: "rank"}

valid_Xover = {pip_crossover: "cross"}

valid_Mutation = {swap_mutation: "swap", insert_mutation: "insert", inversion_mutation: "invert",
                  scramble_mutation: "scramble"}

valid_Replacement = {elitism_replacement: "elit", standard_replacement: "std"}


#Parameters to gridsearch in a run
test_init = [initialize_using_random]
test_select = [roulettewheel_selection]
test_xover = [pip_crossover]
test_mutation = [swap_mutation, insert_mutation, inversion_mutation, scramble_mutation]
test_replacement = [elitism_replacement]
test_xover_prob = [0.1]
test_mut_prob = [0.9]
test_tournament_size = [2, 5, 10]


# Initial params
params = {
        # params
        "Population-Size"           : 40,
        "Number-of-Generations"     : 1000,
        "Crossover-Probability"     : 0.8,
        "Mutation-Probability"      : 0.8,
        "Precision"                 : 0.01,
        "Portfolio-Size"            : 30,
        # operators / approaches
        "Initialization-Approach"   : initialize_using_random,
        "Selection-Approach"        : parent_selection,
        "Tournament-Size"           : 5,
        "Crossover-Approach"        : pip_crossover,
        "Mutation-Approach"         : swap_mutation,
        "Replacement-Approach"      : elitism_replacement
    }


pip_encoding_rule = {
    "Size"          : params["Portfolio-Size"],  # It must be defined by the size of DV (Number of products)
    "Is ordered"    : False,
    "Can repeat"    : True,
    "Data"          : [0, 0],
    "Data Type"     : "",
    "Precision"     : 1/params["Precision"]
}

final_prices = input_space_red_pip(pip_encoding_rule["Size"], closing_prices)
print('Given the chosen parameters, the search space is composed by ',  pip_encoding_rule['Precision'], '^',
      pip_encoding_rule["Size"], ' = ', pip_encoding_rule['Precision']**pip_encoding_rule["Size"])

exp, cov = get_dv_pip(final_prices)

pip_decision_variables = {
    "Expected_Returns": exp,  # The closing prices for each period
    "Covariance_Returns": cov,
    "Risk_Free_Return": 1.53  # US Treasury Bonds according to Bloomberg on 08/01/2020, 18:08
}

# Problem Instance
pip_problem_instance = PortfolioInvestmentProblem(
    decision_variables=pip_decision_variables,
    constraints=pip_constraints,
    encoding_rule=pip_encoding_rule
)

def one_combination():
    """
    Actually runs the algorithm with one set of parameters.
    Names the resume file from parameters of search
    Creates the resume file from all the runs for a set of parameters
    """
    log_base_dir="./log/"       # Base dir for log of initial runs
    if not path.exists(log_base_dir):
        mkdir(log_base_dir)
    all_dir = "./log_all/"      # Base dir for resume the resume files
    if not path.exists(all_dir):
        mkdir(all_dir)

    log_name =  ("I-"    + str(valid_Init.get(params.get("Initialization-Approach"))) +
                "_S-"    + str(valid_Select.get(params.get("Selection-Approach"))) +
                "_C-"    + str(valid_Xover.get(params.get("Crossover-Approach"))) +
                "_M-"    + str(valid_Mutation.get(params.get("Mutation-Approach"))) +
                "_R-"    + str(valid_Replacement.get(params.get("Replacement-Approach"))) +
                "_CP-"   + str((params.get("Crossover-Probability"))) +
                "_MP-"   + str((params.get("Mutation-Probability"))) +
                "_PS-"   + str((params.get("Population-Size"))) +
                "_TS-"   + str((params.get("Tournament-Size"))) +
                "_G-"    + str((params.get("Number-of-Generations")))
                )
    resume_name= f"{all_dir}{log_name}.xlsx"

    # checks if the same run as already been performed, if so, skips it.
    # -----------------
    log_dir = str(log_base_dir) + str(log_name)
    if not path.exists(log_dir):
       mkdir(log_dir)

    runs_made = [f for f in listdir(all_dir) if isfile(join(all_dir, f))]
    if (str(log_name)+".xlsx") in runs_made:
        print (f"Run {log_name}.xlsx already made, skipping")
        return


    # Run the same configuration many times (get distribution)
    #--------------------------------------------------------------------------------------------------
    overall_best_solution = None
    number_of_runs = 30
    for run in range(1, number_of_runs + 1):
        # Genetic Algorithm
        ga = GeneticAlgorithm(
            problem_instance=pip_problem_instance,
            params=params,
            run=run,
            log_name=log_name,
            log_dir=log_base_dir
            )

        ga_observer = LocalSearchObserver(ga)
        ga.register_observer(ga_observer)
        ga.search()
        ga.save_log()

        # find the best solution over the runs
        if run == 1:
            overall_best_solution = deepcopy(ga.best_solution)
        else:
            if ga.best_solution.fitness > overall_best_solution.fitness:
                overall_best_solution = deepcopy(ga.best_solution)

        print('overall_best_solution: ', overall_best_solution.representation)
        print('overall_best_solution fitness, sharpe ratio: ', overall_best_solution.fitness)
        print('overall_best_solution expected return: ', overall_best_solution.exp_return, ', ',
              overall_best_solution.exp_return - overall_best_solution.risk_free, 'above risk free return')
        print('overall_best_solution risk: ', overall_best_solution.risk)

    # Consolidate the runs
    #--------------------------------------------------------------------------------------------------

    log_files = [f for f in listdir(log_dir) if isfile(join(log_dir, f))]
    print(log_files)

    fitness_runs = []
    columns_name = []
    counter = 0
    generations = []

    for log_name in log_files:
        if log_name.startswith('run_'):
            df = pd.read_excel(log_dir + "/" + log_name)
            fitness_runs.append(list(df.Fitness))
            columns_name.append(log_name.strip(".xslx"))
            counter += 1

            if not generations:
                generations = list(df["Generation"])

    #fitness_sum = [sum(x) for x in zip(*fitness_runs)]

    df = pd.DataFrame(list(zip(*fitness_runs)), columns=columns_name)

    fitness_sd   = list(df.std(axis=1))
    fitness_mean = list(df.mean(axis=1))

    #df["Fitness_Sum"] = fitness_sum
    df["Generation"]  = generations
    df["Fitness_SD"]  = fitness_sd
    df["Fitness_Mean"]  = fitness_mean
    df["Fitness_Lower"] = df["Fitness_Mean"] - 1.96 * df["Fitness_SD"] / (number_of_runs ** 0.5)
    df["Fitness_Upper"] = df["Fitness_Mean"] + 1.96 * df["Fitness_SD"] / (number_of_runs ** 0.5)

    #df.to_excel(log_dir + "/all.xlsx", index=False, encoding='utf-8')
    log_name = ("I-" + str(valid_Init.get(params.get("Initialization-Approach"))) +
                "_S-" + str(
                valid_Select.get(params.get("Selection-Approach"))) +  # this one return None because of .select method
                "_C-" + str(valid_Xover.get(params.get("Crossover-Approach"))) +
                "_M-" + str(valid_Mutation.get(params.get("Mutation-Approach"))) +
                "_R-" + str(valid_Replacement.get(params.get("Replacement-Approach"))) +
                "_CP-" + str((params.get("Crossover-Probability"))) +
                "_MP-" + str((params.get("Mutation-Probability"))) +
                "_PS-" + str((params.get("Population-Size"))) +
                "_TS-" + str((params.get("Tournament-Size"))) +
                "_G-" + str((params.get("Number-of-Generations")))
                )

    # Exporting summary of configuration with best solution
    with pd.ExcelWriter(all_dir + f"{log_name}.xlsx") as writer:
        df.to_excel(writer, sheet_name='Fitness', index=False, encoding='utf-8')
        pd.DataFrame([[list(overall_best_solution.representation), overall_best_solution.fitness,
                       overall_best_solution.exp_return, overall_best_solution.risk,
                       (overall_best_solution.exp_return - overall_best_solution.risk_free)]],
                     columns=["Representation", "Fitness, Sharpe Ratio", "Expected Return", "Risk", "Above Risk Free"]).\
            to_excel(writer, sheet_name='Overall_Best_Solution')

# -------------------------------------------------------------------------------------------------
# RUNS Through the Several list of possible parameters
# -------------------------------------------------------------------------------------------------
for init in range(len(test_init)):
    params["Initialization-Approach"] = test_init[init]
    for select in range(len(test_select)):
        params["Selection-Approach"] = test_select[select]
        for xover in range(len(test_xover)):
            params["Crossover-Approach"] = test_xover[xover]
            for mutation in range(len(test_mutation)):
                params["Mutation-Approach"] = test_mutation[mutation]
                for replacement in range(len(test_replacement)):
                    params["Replacement-Approach"] = test_replacement[replacement]
                    for xover_prob in range(len(test_xover_prob)):
                        params["Crossover-Probability"] = test_xover_prob[xover_prob]
                        for mut_prob in range(len(test_mut_prob)):
                            params["Mutation-Probability"] = test_mut_prob[mut_prob]
                            if str(test_select[select]) == str(tournament_selection):
                                for tourn_size in range(len(test_tournament_size)):
                                    params["Tournament-Size"] = test_tournament_size[tourn_size]
                                    one_combination()
                            else:
                                one_combination()

#[sum(sublist) for sublist in itertools.izip(*myListOfLists)]



