/**********************************************************************************
 * Copyright (c) 2023 Process Systems Engineering (AVT.SVT), RWTH Aachen University
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0.
 *
 * SPDX-License-Identifier: EPL-2.0
 *
 **********************************************************************************/

#include "util/visitor_utils.hpp"
#include "expression_utils_is_constant.hpp"

namespace ale {

    /**
     * Checks if a tree contains any parameter_nodes
     */
    struct is_tree_constant_visitor {
        is_tree_constant_visitor(symbol_table& symbols): symbols(symbols) {}

        template <typename TType>
        void operator()(value_node<TType>* node) {
            traverse_children(*this, node, symbols);
        }

        template <typename TType>
        void operator()(function_node<TType>* node) {
            auto* sym = cast_function_symbol<TType>(symbols.resolve(node->name));
            if (sym == nullptr) {
                throw std::invalid_argument("functionsymbol " + node->name + " is ill-defined");
            }

            std::map<std::string, value_node_variant> arg_map;
            auto args = extract_function_arguments(node);
            for (int i = 0; i < args.size(); ++i) {
                arg_map.emplace(sym->arg_names.at(i), args.at(i));
            }

            auto expr_copy = sym->expr;
            replace_parameters(expr_copy, arg_map);

            return call_visitor(*this, expr_copy);
        }

        template <typename TType>
        void operator()(parameter_node<TType>* node) {
            auto* sym = symbols.resolve(node->name);
            call_visitor(*this, sym);
        }

        template <typename TType>
        void operator()(parameter_symbol<TType>* sym) {
            if (sym->m_is_placeholder) {
                is_constant = false;
            }
        }

        template <typename TType>
        void operator()(variable_symbol<TType>* sym) {
            is_constant = false;
        }

        template <typename TType>
        void operator()(expression_symbol<TType>* sym) {
            call_visitor(*this, sym->m_value);
        }

        template <typename TType>
        void operator()(function_symbol<TType>* sym) {
            throw std::invalid_argument("function_symbol should not be encountered");
        }

        bool is_constant = true;
        symbol_table& symbols;
    };

    bool is_tree_constant(value_node_variant node, symbol_table& symbols) {
        is_tree_constant_visitor visitor(symbols);
        call_visitor(visitor, node);

        return visitor.is_constant;
    }

}
